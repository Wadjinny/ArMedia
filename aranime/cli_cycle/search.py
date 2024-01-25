from aranime.provider_wrapper import (
    WitAnime,
    AnimeSanka,
    ZimaBdk,
    AnimeIat,
)
from rich.table import Table
from aranime.utils import zip_extend
from aranime.utils import die
def search_part(anime, console,search_providers):
    columns = ["id"]
    results = []
    animes = []
    to_pop = []
    for i, provider in enumerate(search_providers):
        search_result = provider.search_anime(anime)
        if len(search_result) == 0:
            to_pop.append(i)
            continue

        animes.append(search_result)

        results.append(
            [
                f"{anime_res.name.lower().replace(anime,'[bold #fcfacf]'+anime+'[/]')} [bold yellow]{anime_res.episode_count}EPS[/]"
                for anime_res in search_result
            ]
        )
        columns.append(provider.__name__)

    if len(results) == 0:
        console.print(f'"{anime}" didn\'t get any results')
        return None, None
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
    return columns, animes