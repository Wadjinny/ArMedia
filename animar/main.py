import typer
from rich.console import Console
from animar.provider_wrapper import WitAnime, AnimeSanka, ZimaBdk, ProviderController
from animar.anime_interface import Anime
from rich.table import Table
from rich.prompt import Prompt
from pathlib import Path
from .utils import zip_extend
from time import sleep
from typing_extensions import Annotated

console = Console()


def main(anime_name: Annotated[str, typer.Option(prompt=True)]):
    # name = Prompt.ask("Enter anime name")
    # anime_name = "mf ghost"
    columns = ["id"]

    results = []
    animes = []
    to_pop = []
    search_providers = [
        # WitAnime,
        # AnimeSanka,
        ZimaBdk,
    ]
    for i, provider in enumerate(search_providers):
        search_result = provider.search_anime(anime_name)
        if len(search_result) == 0:
            to_pop.append(i)
            continue

        animes.append(search_result)
        results.append(
            [f"{anime.episode_count} EPS. {anime.name}" for anime in search_result]
        )
        columns.append(provider.__name__)
    if len(results) == 0:
        console.print(f'"{anime_name}" didn\'t get any results')
        return
    for i in to_pop[::-1]:
        search_providers.pop(i)

    table_anime = list(zip_extend(*results))

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
    for i, animes_all in enumerate(table_anime):
        table.add_row(str(i + 1), *animes_all)
    console.print(table)

    while True:
        anime_indecies = Prompt.ask("Choose the anime number")
        # anime_indecies = "0 0 0"
        try:
            anime_indecies = [int(i) for i in anime_indecies.split(" ")]
        except ValueError:
            console.print("you must enter numbers")
            continue

        if len(anime_indecies) != len(columns) - 1:
            console.print(f"you must choose {len(columns) - 1 } animes")
            continue

        if not all(0 <= ind <= len(animes[i]) for i, ind in enumerate(anime_indecies)):
            console.print(f"you must choose animes between 0[deselect] and id of anime")
            continue
        break

    providers = [
        provider_cls(anime[index - 1])
        for provider_cls, anime, index in zip(search_providers, animes, anime_indecies)
        if index != 0
    ]
    console.clear()
    console.print(*providers)
    provider_controller = ProviderController(*providers)

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    for episode in provider_controller.episodes:
        for server in episode.servers:
            with console.status(f"Trying {server}", spinner="dots"):
                if not server.test():
                    continue
            if server.download(output_dir=output_dir):
                break


def run():
    typer.run(main)


if __name__ == "__main__":
    run()
