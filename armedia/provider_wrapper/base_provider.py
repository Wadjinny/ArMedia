from armedia.utils import join_list_of_list, die, debug, zip_extend
from typing import TYPE_CHECKING
from rich.console import Console

if TYPE_CHECKING:
    from ..media_interface import Media, Episode, Server
console = Console()

def index_of(list_str,text):
    # debug("######",list_str=list_str,text=text)
    for i,e in enumerate(list_str):
        if e in text:
            return i
    return -1

class EpisodeController:
    def __init__(
        self, media: "Media", episodes: list["Episode"], number: str, order_list=None
    ) -> None:
        self.media = media
        self.servers: list["Server"] = join_list_of_list(
            episode.find_servers for episode in episodes
        )
        if order_list is None:
            self.servers = sorted(self.servers, key=lambda s: s.priority, reverse=True)
        else:
            def key(s):
                is_server_in_list = index_of(order_list,str(s)) 
                if is_server_in_list == -1:
                    return 999-s.priority
                else:
                    return is_server_in_list
            self.servers = sorted(self.servers, key=key)
        self.is_dowloaded = False
        self.number = number


class Provider:
    providers: list = []

    def __init__(self, media: "Media") -> None:
        self.media = media
        self._episodes = None

    def __init_subclass__(cls) -> None:
        Provider.providers.append(cls)

    def _request_episodes(self) -> list["Episode"]:
        raise NotImplementedError

    def _episode_servers(self, episodes: "Episode") -> list["Server"]:
        raise NotImplementedError

    def request_episodes(self) -> None:
        if self.media.link is None:
            raise ValueError("anime url is None")
        self._episodes = self._request_episodes()

    def episode_servers(self, episode: "Episode") -> list["Server"]:
        servers = self._episode_servers(episode)
        return servers

    @classmethod
    def _search_media(cls, search_term: str) -> list["Media"]:
        raise NotImplementedError

    @classmethod
    def search_media(cls, search_term: str) -> list["Media"]:
        medias: list["Media"] = cls._search_media(search_term)
        medias = [media for media in medias if media.episode_count != 0]
        return medias

    @property
    def episodes(self) -> list["Episode"]:
        if self._episodes is None:
            self._request_episodes()
        return self._episodes

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.media.name})"


class ProviderController:
    def __init__(self, *providers: Provider, servers_order_list=None) -> None:
        self.providers = providers
        for provider in self.providers:
            with console.status(
                f"requesting episodes from {provider.__class__.__name__}"
            ):
                provider.request_episodes()
        self.episodes_len = max([len(provider.episodes) for provider in self.providers])
        self.filter_episodes = None
        self.servers_order_list = servers_order_list

    @property
    def episodes(self):
        if self.episodes_len is None:
            self.episodes_len = len(self.providers[0].episodes)

        episodes_X_provider = list(
            zip_extend(
                *[provider.episodes for provider in self.providers], no_none=True
            )
        )
        # die(episodes_X_provider=episodes_X_provider)
        for i, episodes_for_each_provider in enumerate(episodes_X_provider):
            if self.filter_episodes is not None:
                if i not in self.filter_episodes:
                    continue
            yield EpisodeController(
                self,
                episodes=episodes_for_each_provider,
                number=f"{i+1}",
                order_list=self.servers_order_list,
            )


if __name__ == "__main__":
    test_list = ["p.pollllop.com", "b-g-eu-20.feetcdn.com:2223"]  
    # die(has_str(test_list,"feetcdn.com"))
    # order_list =  ['ok.ru', 'www.ok.ru', 'feetcdn.com', 'pollllop.com']   
    # test_list = ['s.pollllop.com', 'b-g-eu-15.feetcdn.com:2223'] 
    # die(index_of(order_list,test_list[0]))
    # def key(s):
    #     is_server_in_list = index_of(order_list,str(s)) 
    #     if is_server_in_list == -1:
    #         return 999
    #     else:
    #         return is_server_in_list
    # die(key(test_list[1]))
    # test_list = sorted(test_list, key=key)
    # die(sorted_list=test_list)
    