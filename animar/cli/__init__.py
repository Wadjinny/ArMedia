# %%
# import typer
# from rich.console import Console


# def main():
#     pass


# def run():
#     typer.run(main)


# if __name__ == "__main__":
#     run()

# %%
from rich.prompt import Prompt
from time import sleep
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.live import Live
from animar.utils import zip_extend
from animar.provider_wrapper import (
    WitAnime,
    AnimeSanka,
    ZimaBdk,
    ProviderController,
    EpisodeController,
)
from animar.anime_interface import Anime, Episode, Server
from animar.utils.file_downloader import DownloadFile
from animar.utils import die, debug
from pathlib import Path

console = Console()
with console.screen():
    # name = Prompt.ask("Enter anime name")
    name = "one punch"
    columns = ["id"]
    with console.status("Searching...", spinner="bounce"):
        results = []
        witanime = WitAnime.search_anime(name)
        if witanime:
            results.append(anime.name for anime in witanime)
            columns.append("witanime")

        animesanka = AnimeSanka.search_anime(name)
        if animesanka:
            results.append(anime.name for anime in animesanka)
            columns.append("animesanka")

        zimabdk = ZimaBdk.search_anime(name)
        if zimabdk:
            results.append(anime.name for anime in zimabdk)
            columns.append("zimabdk")

        results = list(zip_extend(*results))

    console.clear()

    table = Table(
        *columns,
        title="Found anime",
        show_edge=False,
        show_lines=False,
        show_footer=False,
        row_styles=["", "on #333d3d"],
        expand=True,
    )
    for i, animes_all in enumerate(results):
        table.add_row(str(i), *animes_all)
    console.print(table)

    # anime_indecies = Prompt.ask("Choose the anime number")
    anime_indecies = "0 0 0"
    anime_indecies = [int(i) for i in anime_indecies.split(" ")]
    if len(anime_indecies) != len(columns) - 1:
        raise ValueError(f"you must choose {len(columns)} animes")

    index_witanime, index_animesanka, index_zimabdk = anime_indecies
    providers = [
        WitAnime(witanime[index_witanime]),
        AnimeSanka(animesanka[index_animesanka]),
        ZimaBdk(zimabdk[index_zimabdk]),
    ]
    console.print(providers)

    provider_controller = ProviderController(*providers)

    # Prompt.ask("\n\n\n[bold green] Done! [/]")

    console.clear()

    class EpisodeCli:
        def __init__(self, episode: EpisodeController):
            self.episode = episode
            self.is_downloaded = False
            self.percentage = 0
            self.is_being_downloaded = False

            self.downloader: DownloadFile = None
            self.download_itter = None

        def setup(self):
            output_dir = Path(".")
            for server in self.episode.servers:
                # debug(f"trying {server}")
                if server.test():
                    self.downloader = server.get_downloader(output_dir=output_dir)
                    break
            self.size = self.downloader.total_size
            self.download_itter = self.downloader.download()

        def download(self):
            if self.download_itter is None:
                self.setup()
                self.is_being_downloaded = True
            chunk = next(self.download_itter, None)
            self.percentage = self.downloader.downloaded_size / self.size
            if chunk is None:
                # debug(f"chunk is None: {self.episode.number}")
                self.is_downloaded = True
                self.is_being_downloaded = False
                self.downloader.close()
                return True
            return False
        
        def __repr__(self) -> str:
            return f"EpisodeCli(ep={self.episode.number}, is_downloaded={self.is_downloaded}, is_being_downloaded={self.is_being_downloaded}, percentage={self.percentage:.3f})"

        def panel(self):
            if self.is_being_downloaded:
                style = "bold yellow"
            elif self.is_downloaded:
                style = "bold green"
            else:
                style = "#333d3d"

            title = f"EP {self.episode.number}"
            progress_width = 13
            status = int(self.percentage * progress_width)
            progress = (
                f"[on yellow]{' '*status}[/][bold]{' '*(progress_width - status + 1)}[/] \n {self.percentage:.3f}"
            )
            panel = Panel(
                progress,
                style=style,
                title=title,
            )
            return panel

    class DownloaderCli:
        def __init__(self) -> None:
            self.episodes = [EpisodeCli(ep) for ep in provider_controller.episodes]

            self.is_done = False
            self.episodes_iter = iter(self.episodes)
            self.current_episode:EpisodeCli = next(self.episodes_iter)
            self.is_last = False

        def download(self) -> Table:
            table = Table.grid()
            table.add_column()
            column = Columns(expand=True)
            for ep in self.episodes:
                column.add_renderable(ep.panel())
            if self.current_episode.download():
                self.current_episode = next(self.episodes_iter, None)
                if self.current_episode is None:
                    self.is_done = True
            table.add_row(column)
            # table.add_row("Saving to '/home/anime'")
            return table

    downloader = DownloaderCli()
    output = Panel(downloader.download(), title="Downloading")
    with Live(output) as live:
        while not downloader.is_done:
            output.renderable = downloader.download()


# Prompt.ask("\n\n\n[bold green] Done! [/]")
