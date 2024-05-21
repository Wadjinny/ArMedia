import requests
import base64
import re
from urllib.parse import quote
from bs4 import BeautifulSoup
from armedia.utils import debug, die

site_extension = "pics"


def get_search_results_link(search_term: str) -> list[dict[str, str]]:
    search_term = quote(search_term)
    url = f"https://witanime.{site_extension}/?search_param=animes&s={search_term}"
    response = requests.request("GET", url, timeout=100)
    response = response.text
    soup: BeautifulSoup = BeautifulSoup(response, "html.parser")
    anime_list = soup("div", class_="hover ehover6")
    anime_list = [
        {"name": anime.find("img")["alt"], "link": anime.find("a")["href"]}
        for anime in anime_list
    ]
    return anime_list


def get_episodes_list(anime_link) -> list[str]:
    response = requests.request("GET", anime_link, timeout=100)
    response = response.text
    soup = BeautifulSoup(response, "html.parser")
    episodes = soup.select(".hover.ehover6")
    episodes_info = []
    for episode in episodes:
        link = re.search(
            r"openEpisode\('(.*)'\)", episode.select_one(".overlay")["onclick"]
        ).group(1)
        link = base64.b64decode(link).decode("utf-8")
        number = episode.select_one("h3 > a").text
        number = re.sub(r"[^\x00-\x7f]", r"", number)

        episodes_info.append({"link": link, "number": number})
    return episodes_info


def get_all_episodes_server_link(episode_link):
    # todo: shave headers
    def get_links_from_yonaplay(yonaplay_link, extension):
        yonaplay_link = yonaplay_link + "&apiKey=7d942435-c790-405c-8381-f682a274b437"
        headers = {
            "referer": f"https://witanime.{extension}/",
        }

        payload = {}
        response = requests.request("GET", yonaplay_link, data=payload, headers=headers)

        response = response.text
        server_links = re.findall("go_to_player\('(.*?)'\)", response)
        return server_links

    def get_links_from_soraplay(soraplay_link, extension):
        headers = {"referer": f"https://witanime.{extension}/"}
        response = requests.request("GET", soraplay_link, headers=headers)
        response = response.text
        # go_to_player('//userscloud.com/embed-4z6fyrcnfjns.html')
        server_links = re.findall("go_to_player\('(.*?)'\)", response)
        for i, link in enumerate(server_links):
            if link.startswith("//"):
                server_links[i] = "https:" + link
        return server_links

    payload = {}
    response = requests.request("GET", episode_link, data=payload)
    response = response.text
    soup = BeautifulSoup(response, "html.parser")
    server_links = soup.select("#episode-servers a")
    server_links = [
        base64.b64decode(a["data-url"]).decode("utf-8") for a in server_links
    ]

    download_links = soup.select(".quality-list a")
    download_links = [
        base64.b64decode(a.get("data-url", "")).decode("utf-8") for a in download_links
    ]
    download_links = download_links[::-1]
    server_links.extend(download_links)
    yonaplay_id = list(filter(lambda x: "yonaplay" in x, server_links))
    if yonaplay_id:
        yonaplay_id = yonaplay_id[0]
        extension = re.search(r"witanime\.(.*?)/", episode_link).group(1)
        yonaplay_server_links = get_links_from_yonaplay(yonaplay_id, extension)
        server_links.extend(yonaplay_server_links)
    else:
        # print("no yonaplay")
        debug("no soraplay 'Witanime'")
        pass

    # 'https://soraplay.xyz/embed/5QDgM8nSke17f/mirror
    soraplay_id = list(
        filter(lambda x: re.search(r"soraplay\.xyz/embed/.*/mirror", x), server_links)
    )
    if soraplay_id:
        soraplay_id = soraplay_id[0]
        extension = re.search(r"witanime\.(.*?)/", episode_link).group(1)
        soraplay_server_links = get_links_from_soraplay(soraplay_id, extension)
        server_links.extend(soraplay_server_links)
    else:
        pass

    return server_links


if __name__ == "__main__":
    print(
        get_episodes_list(
            "https://witanime.pics/anime/itsudatte-bokura-no-koi-wa-10-cm-datta/"
        )
    )
