from ..utils import join_list_of_list,die,debug
from typing import TYPE_CHECKING
from rich.console import Console

if TYPE_CHECKING:
    from ..anime_interface import Anime,Episode,Server
console = Console()

class EpisodeController:
    def __init__(self, anime: "Anime", episodes: list["Episode"], number: str) -> None:
        self.anime = anime
        self.servers:list["Server"] = join_list_of_list(episode.find_servers for episode in episodes)
        self.is_dowloaded = False
        self.number = number


class Provider:
    providers: list = []

    def __init__(self, anime:"Anime") -> None:
        self.anime = anime
        self._episodes = None

    def __init_subclass__(cls) -> None:
        Provider.providers.append(cls)

    def _request_episodes(self):
        raise NotImplementedError

    def _episode_servers(self,episodes: "Episode"):
        raise NotImplementedError


    def request_episodes(self):
        if self.anime.link is None:
            raise ValueError("anime url is None")
        self._episodes = self._request_episodes()

    def episode_servers(self, episode:"Episode")->list["Server"]:
        servers = self._episode_servers(episode)
        servers = sorted(servers, key=lambda s: s.priority, reverse=True)
        servers_name = [str(s) for s in servers]
        servers_count = [f"[{servers_name.count(s)}]{s}" for s in set(servers_name)]
        console.print(f"'{self.__class__.__name__}'/'{self.anime.name}'/'EP{episode.number}': '{', '.join(servers_count)}'", markup=False)
        return servers

    @classmethod
    def _search_anime(cls,search_term: str):
        raise NotImplementedError
    
    @classmethod
    def search_anime(cls, search_term: str):
        return cls._search_anime(search_term)
        
    @property
    def episodes(self):
        if self._episodes is None:
            self._request_episodes()
        return self._episodes
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.anime.name})"


class ProviderController:
    def __init__(self, *providers:Provider) -> None:
        self.providers = providers
        for provider in self.providers:
            with console.status(f"requesting episodes from {provider.__class__.__name__}"):
                provider.request_episodes()
        episodes_len = [len(provider.episodes) for provider in self.providers]
        if not all(i == episodes_len[0] for i in episodes_len):
            raise ValueError(f"all providers must have same number of episodes: {episodes_len}, {[p.anime.link for p in self.providers]}")
        self.episodes_len = None

    @property
    def episodes(self):
        if self.episodes_len is None:
            self.episodes_len = len(self.providers[0].episodes)
        for i in range(self.episodes_len):
            episode_for_each_provider = []
            for provider in self.providers:
                episode_for_each_provider.append(provider.episodes[i])
            yield EpisodeController(
                self, episodes=episode_for_each_provider, number=f"{i}"
            )
