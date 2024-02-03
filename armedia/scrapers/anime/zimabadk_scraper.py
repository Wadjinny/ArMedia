import requests
import re
from bs4 import BeautifulSoup
from armedia.utils import debug, die
from urllib.parse import urlencode
import jmespath


def get_search_results_link(search_term: str) -> list[str]:
    types = ["anime"]
    animes = []
    for type in types:
        url = f"https://www.zimabadk.com/ajaxcenter/search"
        headers = {
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        }
        payload = {"s": search_term, "type": type}
        payload = urlencode(payload)
        session = requests.Session()
        response = session.post(url, timeout=100, data=payload, headers=headers)
        response = response.text
        soup = BeautifulSoup(response, "html.parser")
        anime_list = soup.select("a.main--block.before")
        for anime in anime_list:
            name = anime.select_one("post--details>h3").text
            name = re.sub(r"[^\x00-\x7f]", r"", name)
            link = anime["href"]
            animes.append({"name": name, "link": link})
    return animes


def get_episodes_list(anime_link) -> list[str]:
    response = requests.request("GET", anime_link, timeout=100)
    response = response.text
    soup = BeautifulSoup(response, "html.parser")
    # .episodes-list a
    info = soup.select(".episodes-list a")
    # links = [link["href"] for link in links]
    episodes = []
    for i in info:
        number = i.select_one("strong").text
        link = i["href"]
        episodes.append({"number": number, "link": link})
    return episodes[::-1]


def get_all_episodes_server_link(episode_link):
    response = requests.request("GET", episode_link, timeout=100)
    response = response.text
    soup = BeautifulSoup(response, "html.parser")
    server_links = soup.select("servers-links .server")
    server_links = [link["data-code"] for link in server_links]
    download_link = soup.select("download--servers a")
    download_link = [link["href"] for link in download_link]
    for i, link in enumerate(server_links):
        if "megamax.me/iframe" in link:
            link = link.strip()
            response = requests.request("GET", link)
            
            version = re.search(
                r"version&quot;:&quot;(.+?)&quot;", response.text
            )
            if version is not None:
                version = version.group(1)
            else:
                continue
                
            headers = {
                "x-xsrf-token":"eyJpdiI6IjRJNU4xeS91N1ZndU5KNWZZR2pLOGc9PSIsInZhbHVlIjoiWGJ5dStLbTIwTVBrWHBtRTMvaU1vb3V5OEdkd2R0WEpuZ3BEQjFPZG0xU0JQL3Y1N05abU5rT1I2ZFlSVkN3c055UXh5ZzNDZEk2a051KzlObU9Eb29ySUxmQjgzY0FhSHFmN29QRWFzVDVUdHpqRzF3RU1NaTExUlVBcUpPaC8iLCJtYWMiOiJhYjU3MzZhZmJlOGM5MDhmNWU1YmIwZTQ4ZjIxNWIwMWEyMjdhYzFkY2RmZDhiMWVmMzIzODI1ODk2ZDk3ZWQ3IiwidGFnIjoiIn0=",
                "cookie": "XSRF-TOKEN=eyJpdiI6IjRJNU4xeS91N1ZndU5KNWZZR2pLOGc9PSIsInZhbHVlIjoiWGJ5dStLbTIwTVBrWHBtRTMvaU1vb3V5OEdkd2R0WEpuZ3BEQjFPZG0xU0JQL3Y1N05abU5rT1I2ZFlSVkN3c055UXh5ZzNDZEk2a051KzlObU9Eb29ySUxmQjgzY0FhSHFmN29QRWFzVDVUdHpqRzF3RU1NaTExUlVBcUpPaC8iLCJtYWMiOiJhYjU3MzZhZmJlOGM5MDhmNWU1YmIwZTQ4ZjIxNWIwMWEyMjdhYzFkY2RmZDhiMWVmMzIzODI1ODk2ZDk3ZWQ3IiwidGFnIjoiIn0%3D; megamax_session=eyJpdiI6IlJzMGpMREMrMWlUaGlQRGxkeUQrOEE9PSIsInZhbHVlIjoiV2Mxc1B2SFFCNGRmNFU5ZTA0MXZwM3JWZnFRdGc5TzY1dUwyVCs1S0MreXJBYkpNMkczNWNiOVMvYWdoVEJ3MVFQcGFWOE9QOHJ3L1c4R0dydHR4aTcvSmZmYkgyRThsbXJQQ1pNTDdEK1RHU0s2TWhtRzZSa1ZNZGpJSDRWWDUiLCJtYWMiOiJiZjZhNTRiZmMwNGYzZjMxMjkzMmYyOGIxYjU1MzA5NTczN2NlZTNhMzg3MDJlNjUzZGI5ZGYzZDE4ZDU0YTViIiwidGFnIjoiIn0%3D",
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
                continue
            server_links.extend(megamax_servers)
            
    for i, s in enumerate(server_links):
        if s.startswith("//"):
            server_links[i] = "https:" + s

    return server_links + download_link



if __name__=="__main__":
    print(get_episodes_list("https://www.zimabadk.com/anime/migi-to-dali/"))
