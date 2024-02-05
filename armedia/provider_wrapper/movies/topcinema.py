from time import sleep
from rich.console import Console
from ..base_provider import Provider
from armedia.media_interface import Media, Episode, Server
from armedia.scrapers.movies.topcinema_scraper import (
    get_search_results_link,
    get_all_episodes_server_link,
    get_episodes_list,
)
from armedia.utils import wait, die

console = Console()


class TopCinema(Provider):
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
                    episodes = get_episodes_list(media_link=anime.link)
                    anime.episode_count = len(episodes)

        if len(result) == 0:
            console.log(f'media "{search_term}" not found in {cls.__name__}')
            return []
        return result

    def _request_episodes(self) -> list["Episode"]:
        episode_info = get_episodes_list(self.media.link)
        episodes = []
        for ep_info in episode_info:
            episodes.append(Episode(provider=self, **ep_info))
        return episodes

    def _episode_servers(self, episode: Episode) -> list["Server"]:
        servers = get_all_episodes_server_link(episode.link)
        servers = [
            Server(link=server_link, episode=episode)
            for server_link in servers
            if Server.is_downloadable(server_link)
        ]
        return servers
