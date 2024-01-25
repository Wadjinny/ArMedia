from rich.prompt import Prompt
import re


def anime_decision(search_providers, animes, columns, console):
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

        if not all(0 <= ind <= len(animes[i]) for i, ind in enumerate(anime_indecies)):
            console.print(
                f"  :no_entry: You must choose animes between [red]0 [dim]deselect[/] and {len(animes[i])}[/] \n"
            )

            continue

        if all(ind == 0 for ind in anime_indecies):
            console.print("  :no_entry: You must choose [red]at least one anime[/] \n")
            continue
        if (
            len(
                set(
                    animes[i][ind - 1].episode_count
                    for i, ind in enumerate(anime_indecies)
                    if ind != 0
                )
            )
            > 1
        ):
            chosen_anime = '[bold yellow]\n   '+'\n   '.join(animes[i][ind - 1].name for i, ind in enumerate(anime_indecies) if ind != 0)+'[/]'
            console.print(
                f"You have chosen:{chosen_anime}"
            )
            user_choice = Prompt.ask(f" [bold yellow]Mismatch[/] episode count, Do you want to continue? [y/n]",default="n",choices=["y","n"])
            if user_choice == "n":
                continue
        break
    return anime_indecies