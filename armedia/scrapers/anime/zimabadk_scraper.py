import requests
import re
from bs4 import BeautifulSoup
from armedia.utils import debug, die
from urllib.parse import urlencode
import jmespath


def get_search_results_link(search_term: str) -> list[str]:
    types = [
        "movies",
        "anime",
    ]
    animes = []
    for type in types:
        url = f"https://www.zimabadk.com/?type={type}&s={search_term}"
        response = requests.get(url, timeout=100)
        soup = BeautifulSoup(response.text, "html.parser")
        anime_list = soup.select("div.postBlockOne")
        # die(anime_list=anime_list)
        for anime in anime_list:
            name = anime.select_one("h3.title").text.strip()
            name = re.sub(r"[^\x00-\x7f]", r"", name)
            link = anime.select_one("a")["href"]
            animes.append({"name": name, "link": link})
        # debug(url=url, animes=animes)
    return animes


def get_episodes_list(anime_link) -> list[str]:
    response = requests.request("GET", anime_link, timeout=100)
    response = response.text
    soup = BeautifulSoup(response, "html.parser")
    # Find episodes in the all-episodes-list
    episode_items = soup.select(".all-episodes-list li a")
    episodes = []
    for item in episode_items:
        # The episode number is in the <em> tag
        number = item.select_one("em").text.strip()
        link = item["href"]
        episodes.append({"number": number, "link": link})
    # Return episodes in ascending order (oldest first)
    return episodes[::-1]


def get_all_episodes_server_link(episode_link):
    episode_link = episode_link+"watch"
    response = requests.request("GET", episode_link, timeout=100)
    response = response.text
    # search for https://megamax.me/iframe/dYBe2CrlVbKJV"
    megamax_link = re.search(r'"(https://megamax\.me/iframe/[a-zA-Z0-9]+)', response)
    server_links = []
    while True:
        if megamax_link is not None:
            megamax_link = megamax_link.group(1)
            megamax_link = megamax_link.strip()
            response = requests.request("GET", megamax_link)
            response = response.text
            version = re.search(
                r"version&quot;:&quot;(.+?)&quot;", response
            )
            if version is not None:
                version = version.group(1)
                link = megamax_link
            else:
                break
                
            headers = {
                "x-xsrf-token":"eyJpdiI6IjRJNU4xeS91N1ZndU5KNWZZR2pLOGc9PSIsInZhbHVlIjoiWGJ5dStLbTIwTVBrWHBtRTMvaU1vb3V5OEdkd2R0WEpuZ3BEQjFPZG0xU0JRL3Y1N05abU5rT1I2ZFlSVkN3c055UXh5ZzNDZEk2a051KzlObU9Eb29ySUxmQjgzY0FhSHFmN29QRWFzVDVUdHpqRzF3RU1NaTExUlVBcUpPaC8iLCJtYWMiOiJhYjU3MzZhZmJlOGM5MDhmNWU1YmIwZTQ4ZjIxNWIwMWEyMjdhYzFkY2RmZDhiMWVmMzIzODI1ODk2ZDk3ZWQ3IiwidGFnIjoiIn0=",
                "cookie": "XSRF-TOKEN=eyJpdiI6IjRJNU4xeS91N1ZndU5KNWZZR2pLOGc9PSIsInZhbHVlIjoiWGJ5dStLbTIwTVBrWHBtRTMvaU1vb3V5OEdkd2R0WEpuZ3BEQjFPZG0xU0JRL3Y1N05abU5rT1I2ZFlSVkN3c055UXh5ZzNDZEk2a051KzlObU9Eb29ySUxmQjgzY0FhSHFmN29QRWFzVDVUdHpqRzF3RU1NaTExUlVBcUpPaC8iLCJtYWMiOiJhYjU3MzZhZmJlOGM5MDhmNWU1YmIwZTQ4ZjIxNWIwMWEyMjdhYzFkY2RmZDhiMWVmMzIzODI1ODk2ZDk3ZWQ3IiwidGFnIjoiIn0%3D; megamax_session=eyJpdiI6IlJzMGpMREMrMWlUaGlQRGxkeUQrOEE9PSIsInZhbHVlIjoiV2Mxc1B2SFFCNGRmNFU5ZTA0MXZwM3JWZnFRdGc5TzY1dUwyVCs1S0MreXJBYkpNMkczNWNiOVMvYWdoVEJ3MVFQcGFWOE9QOHJ3L1c4R0dydHR4aTcvSmZmYkgyRThsbXJQQ1pNTDdEK1RHU0s2TWhtRzZSa1ZNZGpJSDRWWDUiLCJtYWMiOiJiZjZhNTRiZmMwNGYzZjMxMjkzMmYyOGIxYjU1MzA5NTczN2NlZTNhMzg3MDJlNjUzZGI5ZGYzZDE4ZDU0YTViIiwidGFnIjoiIn0%3D",
                "x-inertia": "true",
                "x-inertia-partial-component": "files/mirror/video",
                "x-inertia-partial-data": "streams",
                "x-inertia-version": version,
            }
            response = requests.request("GET", link, headers=headers)
            path = "@.props.streams.data[].mirrors[].link"
            megamax_servers = jmespath.search(path, response.json())
            if megamax_servers is None:
                print("In Zimabadk_scraper.py: megamax servers if failing (Maybe xsrf token is expired)",f'{megamax_servers=}')
                break
            server_links.extend(megamax_servers)
            break
            
    for i, s in enumerate(server_links):
        if s.startswith("//"):
            server_links[i] = "https:" + s

    return server_links



if __name__=="__main__":
    # print(get_search_results_link("naruto"))
    # print(get_episodes_list("https://www.zimabadk.com/anime/migi-to-dali/"))
    print(get_all_episodes_server_link("https://www.zimabadk.com/migi-to-dali-%d8%a7%d9%84%d8%ad%d9%84%d9%82%d8%a9-1/"))