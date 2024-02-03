from rich.prompt import Prompt
import re
from armedia.utils import zip_extend, die, debug
from armedia.provider_wrapper import (
    WitAnime,
    AnimeSanka,
    ZimaBdk,
    AnimeIat,
    TopCinema,
)

def media_decision(search_providers, medias, columns, console):
    while True:
        anime_indecies = Prompt.ask("\n[bold]Choose the anime number[/]")
        anime_indecies = anime_indecies.strip()
        anime_indecies = re.sub(r"\s+", " ", anime_indecies)
        try:
            anime_indecies = [int(i) for i in anime_indecies.split(" ")]
        except ValueError:
            console.print("  :no_entry: You must enter [red]numbers[/] \n")
            continue

        if len(anime_indecies) == 1:
            anime_indecies = anime_indecies * len(search_providers)

        if len(anime_indecies) != len(columns) - 1:
            console.print(
                f"  :no_entry: You must choose [red]{len(columns) - 1 } animes[/] \n"
            )
            continue

        if not all(0 <= ind <= len(medias[i]) for i, ind in enumerate(anime_indecies)):
            console.print(
                f"  :no_entry: You must choose animes between [red]0 [dim]deselect[/] and {len(medias[i])}[/] \n"
            )

            continue

        if all(ind == 0 for ind in anime_indecies):
            console.print("  :no_entry: You must choose [red]at least one anime[/] \n")
            continue
        if (
            len(
                set(
                    medias[i][ind - 1].episode_count
                    for i, ind in enumerate(anime_indecies)
                    if ind != 0
                )
            )
            > 1
        ):
            chosen_anime = (
                "[bold yellow]\n   "
                + "\n   ".join(
                    medias[i][ind - 1].name
                    for i, ind in enumerate(anime_indecies)
                    if ind != 0
                )
                + "[/]"
            )
            console.print(f"You have chosen:{chosen_anime}")
            user_choice = Prompt.ask(
                f" [bold yellow]Mismatch[/] episode count, Do you want to continue? [y/n]",
                default="n",
                choices=["y", "n"],
            )
            if user_choice == "n":
                continue
        break
    return anime_indecies


def choose_provider(filter_str,providers_list):
    """filter : 'awizt' or 'anime' or 'media'
    [
        AnimeSanka,
        WitAnime,
        AnimeIat,
        ZimaBdk,
        TopCinema,
    ]
    """
    providers_map = {
        AnimeSanka:"a",
        WitAnime:"w",
        AnimeIat:"i",
        ZimaBdk:"z",
        TopCinema:"t",
    }
    providers_chars = "".join(providers_map.values())
    anime_p = "awiz"
    media_p = "t"
    if filter_str == "media":
        return [p for p in providers_list if providers_map.get(p) in media_p]
    elif filter_str == "anime":
        return [p for p in providers_list if providers_map.get(p) in anime_p]
    else:
        return [p for p in providers_list if providers_map.get(p) in filter_str]


if __name__ == "__main__":
    providers_list = [
        AnimeSanka,
        # WitAnime,
        AnimeIat,
        # ZimaBdk,
        TopCinema,    
    ]
        
    test_list = ["awi", "w", "anime", "media"]
    
    for t in test_list:
        debug(t, "=", choose_provider(t,providers_list))
