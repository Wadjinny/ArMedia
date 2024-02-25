from .base_provider import Provider
from ..utils import debug, die
from ..downloaders import (
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
    doodstream,
    streamtape,
    downet,
    pollllop,
)
import re
from tqdm import tqdm


class Media:
    def __init__(
        self, name: str, link=None, episode_count=None, meta=None
    ):
        self.name = name
        self.link = link
        self.episode_count = episode_count
        self.meta = meta

    @staticmethod
    def search(media_name: StopIteration):
        result = search_media(media_name)
        result = [Media(**i) for i in result]
        return result[:10]

    def __repr__(self) -> str:
        base = f"Media("
        for k, v in self.__dict__.items():
            if v is None:
                continue
            base += f"{k} = {v},"
        base = base[:-1]
        base += " )"
        return base


class Episode:
    def __init__(
        self, provider: Provider, link: str = None, number: str = None, servers=None,meta=None
    ):
        self.link = link
        self.number = number
        self.provider = provider
        self._servers = servers
        self.meta = meta

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
        self.file_name = f"{self.episode.provider.media.name}_EP{self.episode.number}.mp4"
        self.file_name = re.sub(r'[<>:"/\\|?*]', "", self.file_name)

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
            doodstream,
            streamtape,
            downet,
            pollllop,
        ]
        for downloader in available_downloaders:
            if downloader.filter_function(link):
                return downloader
        return False

    def test(self):
        return self.downloader.download(self.link, None, None, return_url=True)

    def download(self, output_dir):
        desc = f"EP{self.episode.number}:{self}"
        return self.downloader.download(self.link, output_dir, self.file_name, desc=desc)
