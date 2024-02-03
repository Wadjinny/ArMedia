import asyncio
from tqdm import tqdm
import httpx
from pathlib import Path
import logging
from rich.console import Console
import sniffio
from armedia.utils import die, debug

logging.getLogger("httpx").setLevel(logging.WARNING)
console = Console()

async def maybe_coro(coro, *args, **kwargs):
    loop = asyncio.get_running_loop()

    if asyncio.iscoroutinefunction(coro):
        return await coro(*args, **kwargs)
    else:
        return await loop.run_in_executor(None, coro, *args, **kwargs)


class MultiConnectionDownloader:
    MINIMUM_PART_SIZE = 1024**2

    def __init__(
        self,
        session,
        *args,
        loop=None,
        progress_bar=None,
        **kwargs,
    ):
        self.session = session

        self.args = args
        self.kwargs = kwargs

        self.loop = loop or asyncio.new_event_loop()
        self.io_lock = asyncio.Lock()

        self.progress_bar = progress_bar

    async def download_part(
        self,
        io,
        start: int,
        end: int,
        progress_bar=None,
        future=None,
        pause_event=None,
    ):
        headers = self.kwargs.pop("headers", {})
        content_length = end
        position = start or 0

        is_incomplete = lambda: content_length is None or position < content_length
        is_downloading = lambda: (pause_event is None or not pause_event.is_set())

        while is_downloading() and is_incomplete():
            if content_length is None:
                if start is not None:
                    headers["Range"] = f"bytes={position}-"
            else:
                headers["Range"] = f"bytes={position}-{content_length}"

            try:
                async with self.session.stream(
                    *self.args, **self.kwargs, headers=headers
                ) as response:
                    content_length = (
                        int(response.headers.get("Content-Length", 0)) or None
                    )

                    if progress_bar is not None:
                        if content_length > 0:
                            progress_bar.total = content_length

                    async for chunk in response.aiter_bytes(8192):
                        chunk_size = len(chunk)

                        if self.progress_bar is not None:
                            self.progress_bar.update(chunk_size)

                        if progress_bar is not None:
                            progress_bar.update(chunk_size)

                        await self.write_to_file(
                            self.io_lock,
                            io,
                            position,
                            chunk,
                        )
                        position += chunk_size

                        if not is_downloading():
                            break

                    if content_length is None:
                        content_length = position

            except httpx.HTTPError as e:
                locks = ()
                if progress_bar is not None:
                    locks += (progress_bar.get_lock(),)
                if self.progress_bar is not None:
                    locks += (self.progress_bar.get_lock(),)
                # TODO: Warn user about the error.
            except sniffio.AsyncLibraryNotFoundError:
                console.print(f" [bold red]Stoping[/] the download")
            except KeyboardInterrupt:
                console.print(f" [bold red]Stoping[/] the download")
                break
                

        if future is not None:
            future.set_result((start, position))

        return (start, position)

    @staticmethod
    async def write_to_file(
        lock: asyncio.Lock,
        io,
        position: int,
        data: bytes,
    ):
        async with lock:
            await maybe_coro(io.seek, position)
            await maybe_coro(io.write, data)
            await maybe_coro(io.flush)

    async def allocate_downloads(
        self,
        io,
        content_length: int = None,
        connections: int = 8,
        allocate_content_on_disk=False,
        pause_event=None,
    ):
        def iter_allocations():
            if content_length is None or content_length < self.MINIMUM_PART_SIZE:
                yield None, None
            else:
                chunk_size = content_length // connections
                for i in range(connections - 1):
                    yield i * chunk_size, (i + 1) * chunk_size - 1

                yield (connections - 1) * chunk_size, None

        if allocate_content_on_disk:
            async with self.io_lock:
                await maybe_coro(io.truncate, content_length)

        return await asyncio.gather(
            *(
                self.download_part(io, start, end, pause_event=pause_event)
                for start, end in iter_allocations()
            )
        )

    @staticmethod
    async def is_resumable(
        session,
        method,
        *args,
        **kwargs,
    ):
        headers = kwargs.pop("headers", {})

        headers["Range"] = "bytes=0-0"

        async with session.stream(method, *args, **kwargs) as response:
            return {
                "status_code": response.status_code,
                "headers": response.headers,
                "url": response.url,
            }


async def download_async(
    url, output_dir, file_name=None, session=None, desc=None, CONNECTIONS=32
):
    headers = None if session is None else session.headers
    session = httpx.AsyncClient(
        timeout=30.0,
        follow_redirects=True
    )
    session.headers.update(headers)
    progress_bar = tqdm(
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
    )
    try:
        head_response = await session.head(url)
    except httpx.ConnectTimeout:
        console.print(f" [bold red]Connection Timeout[/]")
        return False
    content_length = int(head_response.headers.get("Content-Length", 0))
    # content_length is under 10mb
    if content_length < 10 * 1024 * 1024:
        # raise Exception(f"{url} is under 10mb: {content_length//1024}kb")
        console.print(f" The file is under 10mb: [bold red]{content_length//1024}kb[/], Skipping...")
        return False
    if file_name is None:
        disposition = head_response.headers.get("content-Disposition").split("; ")
        for i in disposition:
            if "filename" in i:
                file_name = i.split("=")[1].replace('"', "")
                break
        else:
            raise Exception("No filename found: Downloader")

    # Set the file path
    temp_file_path = Path(output_dir) / f"{file_name}.temp"
    file_path = Path(output_dir) / file_name

    progress_bar.total = content_length
    progress_bar.set_description(desc)

    with open(temp_file_path, "wb") as io:
        downloader = MultiConnectionDownloader(
            session,
            "GET",
            url,
            progress_bar=progress_bar,
        )

        downloaded_positions = await downloader.allocate_downloads(
            io, content_length, connections=CONNECTIONS
        )
    await session.aclose()
    temp_file_path.rename(file_path)
    return downloaded_positions


def download_file(url, output_dir, file_name=None, session=None, desc=None, CONNECTIONS=32):

    loop = asyncio.new_event_loop()
    value = loop.run_until_complete(download_async(url, output_dir, file_name, session, desc, CONNECTIONS))
    loop.close()
    return value


if __name__ == "__main__":
    link = "https://releases.ubuntu.com/22.04.3/ubuntu-22.04.3-desktop-amd64.iso"
    download_file(link, ".", "test.iso")
