from time import sleep
from rich.console import Console
from ..base_provider import Provider
from armedia.provider_wrapper.media_interface import Media, Episode, Server
from armedia.scrapers.movies.winnoise_scraper import (
    get_search_results_link,
    get_all_episodes_server_link,
    get_episodes_list,
)
from armedia.utils import wait, die, debug
from armedia.utils.add_sub import add_subtitles_to_video
import requests

console = Console()

rabbit_headers = {
    "authority": "i.pollllop.com",
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "origin": "https://rabbitstream.net",
    "Referer": "https://rabbitstream.net/",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
}


class WinnoiseServer(Server):
    def __init__(self, link: str, episode: Episode = None, captions=None) -> None:
        super().__init__(link, episode)
        self.captions = captions

    def download(self, output_dir: str) -> None:
        session = requests.Session()
        for caption in self.captions:
            url = caption["file"]
            extention = url.split(".")[-1]
            response = session.get(url, timeout=100)
            caption_path = output_dir / "captions"
            caption_path.mkdir(parents=True, exist_ok=True)
            with open(caption_path / f"{caption['label']}.{extention}", "wb") as f:
                f.write(response.content)
                
        download_status = super().download(output_dir)
        if not download_status:
            return
        debug(srt_files=list(caption_path.glob("*")))
        add_subtitles_to_video(output_dir / self.file_name,srt_files=list(caption_path.glob("*")))
        
        #clean up
        for caption in caption_path.glob("*"):
            caption.unlink()
        caption_path.rmdir()
        
        return download_status


class Winnoise(Provider):
    def __init__(self, anime: Media) -> None:
        super().__init__(anime)

    @classmethod
    def _search_media(cls, search_term: str, show_episode_count=True) -> list["Media"]:
        result = get_search_results_link(search_term)
        result = [Media(name=i["name"], link=i["id"], meta=i) for i in result]
        if show_episode_count:
            for i, anime in enumerate(result):
                with console.status(
                    f"getting episode count for {cls.__name__}/{search_term}: [bold]{i+1}[/]/{len(result)}"
                ):
                    episodes = get_episodes_list(media_desc=anime.meta)
                    anime.episode_count = len(episodes)

        if len(result) == 0:
            console.log(f'media "{search_term}" not found in {cls.__name__}')
            return []
        return result

    def _request_episodes(self) -> list["Episode"]:
        episode_info = get_episodes_list(media_desc=self.media.meta)
        episodes = []
        for ep_info in episode_info:
            episodes.append(
                Episode(
                    provider=self,
                    link=ep_info["id"],
                    number=ep_info["number"],
                    meta=ep_info,
                )
            )
        return episodes

    def _episode_servers(self, episode) -> list["Server"]:
        media_servers = get_all_episodes_server_link(episodes_desc=episode.meta)
        media_servers = [
            WinnoiseServer(
                link=server["link"], captions=server["captions"], episode=episode
            )
            for server in media_servers
            if Server.is_downloadable(server["link"])
        ]
        return media_servers
