import re
import typer
from time import sleep
from pathlib import Path
from typing_extensions import Annotated
from typing import Optional
from rich.console import Console
from rich.prompt import Prompt
from rich.prompt import Prompt
from armedia.provider_wrapper import (
    WitAnime,
    AnimeSanka,
    ZimaBdk,
    AnimeIat,
    TopCinema,
    Akwam,
    Winnoise,
    ProviderController,
    Provider,
)
from armedia.cli_cycle import search_part, media_decision,choose_provider
from armedia.provider_wrapper.media_interface import Media
from .utils import zip_extend, die, filter_list


console = Console()

app = typer.Typer(pretty_exceptions_show_locals=False)


@app.command()
def main(
    search_name: Annotated[str, typer.Option("-s","--search",prompt=True,help="Search for a movie or series")],
    path=typer.Option(None, envvar="ARMEDIA_PATH"),
    r: Annotated[bool,typer.Option( "--range", "-r", help="Choose the episode range")] = False,
    servers_order_file: Annotated[
        Optional[Path],
        typer.Option(
            "--priority", "-p", help="Choose the priority of servers", exists=True
        ),
    ] = None,
    providers_choice :Annotated[Optional[str],typer.Option('--provider-choice','-c',help="Choose which source to search: a[AnimeSanka]w[Witanime]i[Animeiat]z[Zimabadk]t[TopCinema]k[Akwam]")] = "anime"
):
    search_providers = [
        AnimeSanka,
        WitAnime,
        AnimeIat,
        ZimaBdk,
        TopCinema,
        Akwam,
        Winnoise,
    ]
    
    search_providers = choose_provider(providers_choice,search_providers)
    columns, medias = search_part(
        media=search_name, console=console, search_providers=search_providers
    )
    if columns is None:
        return

    medias_indecies = media_decision(
        search_providers=search_providers,
        medias=medias,
        columns=columns,
        console=console,
    )

    providers:list[Provider] = [
        provider_cls(media[index - 1])
        for provider_cls, media, index in zip(search_providers, medias, medias_indecies)
        if index != 0
    ]

    if servers_order_file is not None:
        with servers_order_file.open() as f:
            temp_order_list = f.read().splitlines()
            temp_order_list = [
                i.strip() for i in temp_order_list if not i.startswith("#")
            ]
    else:
        temp_order_list = None
    provider_controller = ProviderController(
        *providers, servers_order_list=temp_order_list
    )

    if r:
        filter_exp = Prompt.ask("\n[bold]Choose the episode range (e.g 1,3-6,8,-5)[/]")
        episode_indecies = filter_list(
            range(provider_controller.episodes_len), filter_exp
        )
        provider_controller.filter_episodes = episode_indecies

    console.clear()

    dir_name = min([p.media.name for p in providers], key=len)

    dir_name = re.sub(r'[<>:"/\\|?*]', "", dir_name)

    if path is not None:
        output_dir = Path(path) / dir_name
    else:
        output_dir = Path(dir_name)

    output_dir.mkdir(parents=True, exist_ok=True)

    console.print(
        "[bold yellow]Providers: [/]", *[p.__class__.__name__ for p in providers]
    )
    console.print("[bold yellow]Output dir:[/] ", f"'{output_dir.absolute()}'")

    for i, episode in enumerate(provider_controller.episodes):
        for i, server in enumerate(episode.servers):
            available_servers = [
                f"[dim]{s}[/]" if j != i else f"[bold]{s}[/]"
                for j, s in enumerate(episode.servers)
            ]
            available_servers = " ".join(available_servers)
            with console.status(
                f"Trying {available_servers}: [bold green]{server.episode.provider.__class__.__name__}[/]",
                spinner="dots",
            ):
                if not server.test():
                    sleep(1)
                    continue

            console.print(
                f"[green]{server.episode.provider.__class__.__name__}[/] / [green]EP{episode.number}->{provider_controller.episodes_len}[/]: {available_servers}",
                # markup=False,
            )
            if server.download(output_dir=output_dir):
                break
            console.print(f"[bold red]Skipping server[/]")
        else:
            console.print(f"[bold red]No server available for EP{episode.number}[/]")


def run():
    app()


if __name__ == "__main__":
    run()
