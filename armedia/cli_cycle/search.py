from armedia.provider_wrapper import (
    Provider
)
from rich.table import Table
from armedia.utils import zip_extend
from armedia.utils import die


def search_part(media, console, search_providers: list[Provider]):
    columns = ["id"]
    results = []
    medias = []
    to_pop = []
    for i, provider in enumerate(search_providers):
        search_result = provider.search_media(media)
        if len(search_result) == 0:
            to_pop.append(i)
            continue

        medias.append(search_result)

        results.append(
            [
                f"{media_result.name.lower().replace(media,'[bold #fcfacf]'+media+'[/]')} [bold yellow]{media_result.episode_count}EPS[/]"
                for media_result in search_result
            ]
        )
        columns.append(provider.__name__)

    if len(results) == 0:
        console.print(f'"{media}" didn\'t get any results')
        return None, None
    for i in to_pop[::-1]:
        search_providers.pop(i)

    table_media = list(zip_extend(*results))
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
    for i, all_medias in enumerate(table_media):
        table.add_row(str(i + 1), *all_medias)
    console.print(table)
    return columns, medias
