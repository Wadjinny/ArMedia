from time import sleep
from rich.console import Console
from .base_provider import Provider
from ..anime_interface import Anime, Episode, Server
from ..scrapers.witanime_scraper import (
    get_search_results_link,
    get_all_episodes_server_link,
    get_episodes_list,
)
from ..utils import wait,die

console = Console()


class WitAnime(Provider):
    def __init__(self, anime: Anime) -> None:
        super().__init__(anime)

    @classmethod
    def _search_anime(cls, search_term: str):
        result = get_search_results_link(search_term)
        result = [Anime(**i) for i in result]
        with console.status(f"getting episode count for {cls.__name__}/{search_term}"):
            for anime in result:
                episodes = get_episodes_list(anime_link=anime.link)
                anime.episode_count = len(episodes)
        if len(result) == 0:
            console.log(f'anime "{search_term}" not found in witanime')
            return []
        return result

    def _request_episodes(self):
        episode_info = get_episodes_list(self.anime.link)
        episodes = []
        for ep_info in episode_info:
            episodes.append(Episode(provider=self, **ep_info))
        return episodes

    def _episode_servers(self, episode: Episode) -> list["Server"]:
        servers = get_all_episodes_server_link(episode.link)
        servers = [Server(link=server_link,episode=episode) for server_link in servers if Server.is_downloadable(server_link)]
        return servers
