from time import sleep
from rich.console import Console
from ..base_provider import Provider
from armedia.provider_wrapper.media_interface import Media, Episode, Server
from armedia.utils import wait, die, debug
from pdb import set_trace
from armedia.scrapers.anime.anime_sanka_scraper import (
    get_search_results_link,
    get_all_episodes_server_link,
)

console = Console()


class AnimeSanka(Provider):
    def __init__(self, anime: Media) -> None:
        super().__init__(anime)

    @classmethod
    def _search_media(cls, search_term: str, show_episode_count=True) -> list["Media"]:
        result = get_search_results_link(search_term)
        result = [Media(**i) for i in result]

        if show_episode_count:
            for i, anime in enumerate(result):
                with console.status(
                    f"getting episode count for {cls.__name__}/{search_term}: [bold]{i+1}[/]/{len(result)}"
                ):
                    episodes = get_all_episodes_server_link(anime_link=anime.link)
                    anime.episode_count = len(episodes)

        if len(result) == 0:
            console.log(f'anime "{search_term}" not found in anime-sanka')
            return []
        result = sorted(result, key=lambda x: abs(len(x.name) - len(search_term)))
        return result

    def _request_episodes(self) -> list["Episode"]:
        episode_info = get_all_episodes_server_link(self.media.link)
        # die(episode_info)
        episodes: list[Episode] = []
        
        for number, server_links in episode_info:
            episode = Episode(provider=self, number=number)
            servers = [
                Server(link=server_link, episode=episode)
                for server_link in server_links
                if Server.is_downloadable(server_link)
            ]
            episode._servers = servers
            episodes.append(episode)
        return episodes
