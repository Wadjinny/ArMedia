from .provider_wrapper.base_provider import Provider
from .scrapers.animewave_scraper import search_anime
from .utils import debug, die
from .downloaders import (
    drive,
    mediafire,
    meganz,
    dropbox,
    okru,
    uploadourvideo,
    soraplay,
    stream_wish,
    shahidha,
    ds2play,
)
import re
from tqdm import tqdm


class Anime:
    def __init__(
        self, name: str, english_name: str = None, link=None, episode_count=None
    ):
        self.name = name
        self.link = link
        self.episode_count = episode_count

    @staticmethod
    def search(anime_name: StopIteration):
        result = search_anime(anime_name)
        result = [Anime(**i) for i in result]
        return result[:10]

    def __repr__(self) -> str:
        base = f"Anime("
        for k, v in self.__dict__.items():
            if v is None:
                continue
            base += f"{k} = {v},"
        base = base[:-1]
        base += ")"
        return base


class Episode:
    def __init__(
        self, provider: Provider, link: str = None, number: str = None, servers=None
    ):
        self.link = link
        self.number = number
        self.provider = provider
        self._servers = servers

    @property
    def find_servers(self):
        if self._servers is None:
            return self.provider.episode_servers(self)
        else:
            return self._servers

    def __repr__(self) -> str:
        base = f"Episode("
        for k, v in self.__dict__.items():
            if v is None:
                continue
            base += f"{k} = {v},"
        base = base[:-1]
        base += ")"
        return base


class Server:
    def __init__(self, link: str, episode: Episode = None):
        self.episode = episode
        self.link = link
        self.downloader = self.is_downloadable(self.link)
        self.priority = self.downloader.priority

    def __repr__(self) -> str:
        repr = re.findall(r"//(.*?)/", self.link)[0]
        return repr

    @staticmethod
    def is_downloadable(link):
        available_downloaders = [
            drive,
            mediafire,
            meganz,
            okru,
            uploadourvideo,
            soraplay,
            dropbox,
            stream_wish,
            shahidha,
            ds2play,
        ]
        for downloader in available_downloaders:
            if downloader.filter_function(link):
                return downloader
        return False

    def test(self):
        return self.downloader.download(self.link, None, None, return_url=True)

    def download(self, output_dir):
        file_name = f"{self.episode.provider.anime.name}_EP{self.episode.number}.mp4"
        file_name = re.sub(r'[<>:"/\\|?*]', '', file_name)
        desc = f"EP{self.episode.number}:{self}"

        return self.downloader.download(self.link, output_dir, file_name, desc=desc)

    # def get_downloader(self, output_dir):
    #     file_name = f"{self.episode.provider.anime.name}_EP{self.episode.number}.mp4"
    #     download_link = self.downloader.get_download_url(self.link)
    #     dowloader = DownloadFile(download_link, output_dir, file_name)
    #     return dowloader
