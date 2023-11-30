import typer
from rich.console import Console
from aranime.provider_wrapper import (
    WitAnime,
    AnimeSanka,
    ZimaBdk,
    AnimeIat,
    EgyDead,
    ProviderController,
    EpisodeController,
)
from aranime.anime_interface import Anime
from rich.table import Table
from rich.prompt import Prompt
from pathlib import Path
from .utils import zip_extend, die
from time import sleep
from typing_extensions import Annotated

console = Console()

app = typer.Typer(pretty_exceptions_show_locals=False)

@app.command()
def main(anime: Annotated[str, typer.Option(prompt=True)],path=typer.Option(None,envvar="ARANIM_PATH"),witanime:bool=True,animarsanka:bool=True,zimabdk:bool=True):
    columns = ["id"]

    results = []
    animes = []
    to_pop = []
    search_providers = [
        AnimeSanka,
        WitAnime,
        ZimaBdk,
        AnimeIat,
        # EgyDead,
    ]
    for i, provider in enumerate(search_providers):
        search_result = provider.search_anime(anime)
        if len(search_result) == 0:
            to_pop.append(i)
            continue

        animes.append(search_result)
        results.append(
            [f"{anime.name} [bold yellow]{anime.episode_count}EPS[/]" for anime in search_result]
        )
        columns.append(provider.__name__)
    if len(results) == 0:
        console.print(f'"{anime}" didn\'t get any results')
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
        row_styles=["", "white on #333d3d"],
        expand=True,
    )
    for i, animes_all in enumerate(table_anime):
        table.add_row(str(i + 1), *animes_all)
    console.print(table)

    while True:
        anime_indecies = Prompt.ask("Choose the anime number")
        try:
            anime_indecies = [int(i) for i in anime_indecies.split(" ")]
        except ValueError:
            console.print("you must enter numbers")
            continue

        if len(anime_indecies) == 1:
            anime_indecies = anime_indecies * len(search_providers)
            
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
    provider_controller = ProviderController(*providers)
    
    names = [p.anime.name for p in providers]
    output_dir = Path(f"{names[0]}")
    
    if path is not None:
        output_dir = Path(path) / output_dir
        
    console.print("[bold yellow]Providers: [/]",*[p.__class__.__name__ for p in providers])
    console.print("[bold yellow]Output dir:[/] ",f"'{output_dir.absolute()}'")
    
    for i,episode in enumerate(provider_controller.episodes):  
        for i,server in enumerate(episode.servers):
            with console.status(f"Trying {server} :{i+1}/{len(episode.servers)}: {server.episode.provider.__class__.__name__}", spinner="dots"):
                if not server.test():
                    continue

            console.print(
                f"'{server.episode.provider.__class__.__name__}'/'EP{episode.number}': '{server}'",
                markup=False,
            )
            if server.download(output_dir=output_dir):
                break


def run():
    app()


if __name__ == "__main__":
    run()
