import requests
import base64
import re
from urllib.parse import quote
from bs4 import BeautifulSoup
from armedia.utils import debug, die


def get_search_results_link(search_term: str) -> list[dict[str, str]]:
    search_term = quote(search_term)
    url = "https://web.topcinema.cam/wp-content/themes/movies2023/Ajaxat/Searching.php"
    headers = {
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Referer": "https://web.topcinema.cam/",
    }
    body = f"search={search_term}+&type=all"
    response = requests.request("POST", url, headers=headers, data=body, timeout=100)
    response = response.text
    soup: BeautifulSoup = BeautifulSoup(response, "html.parser")
    titles = soup.select("ul > div")
    titles_formated = []
    for title in titles:
        link = title.select_one("a")["href"]
        if "/series/" in link:
            response = requests.request("GET", link, timeout=100)
            soup = BeautifulSoup(response.text, "html.parser")
            seasons = soup.select("section.allseasonss .Small--Box.Season")
            for season in seasons:
                season_name = season.select_one("h3.title").text
                season_name = re.sub(r"[^\x00-\x7f]", r"", season_name).strip()
                season_number = season.select_one(".epnum").text
                season_number = re.sub(r"^[^a-zA-Z0-9]+", "", season_number).strip()
                season_link = season.select_one("a")["href"]
                titles_formated.append(
                    {
                        "name": f"{season_name} season {season_number}",
                        "link": season_link,
                    }
                )
        else:
            name = title.select_one("h3.title").text
            name = re.sub(r"[^\x00-\x7f]", r"", name)
            name = name.strip()
            titles_formated.append({"name": name, "link": link})

    return titles_formated[::-1]


def get_episodes_list(media_link) -> list[str]:
    if "/series/" not in media_link:
        return [{"link": media_link, "number": "1"}]
    response = requests.request("GET", media_link, timeout=100)
    response = response.text
    soup = BeautifulSoup(response, "html.parser")
    episodes = soup.select("section.allepcont.getMoreByScroll > .row > a")
    episodes_info = []
    for episode in episodes:
        link = episode["href"]
        number = episode.select_one(".epnum").text
        number = re.sub(r"^[^a-zA-Z0-9]+", "", number)
        episodes_info.append({"link": link, "number": number})
    return episodes_info[::-1]


def get_all_episodes_server_link(episode_link):
    # todo: shave headers
    episode_link = episode_link + "/watch/"
    response = requests.request("GET", episode_link, timeout=100)
    response = response.text
    soup = BeautifulSoup(response, "html.parser")
    servers_ids = soup.select(".watch--servers--list > ul > li")
    servers_ids = [(sid["data-id"], sid["data-server"]) for sid in servers_ids]
    url = "https://web.topcinema.cam/wp-content/themes/movies2023/Ajaxat/Single/Server.php"
    headers = {
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "referer": "https://web.topcinema.cam/",
        "x-requested-with": "XMLHttpRequest",
    }
    servers_link = []
    for id, server in servers_ids:
        body = f"id={id}&i={server}"
        response = requests.request(
            "POST", url, headers=headers, data=body, timeout=100
        )
        response = response.text
        soup = BeautifulSoup(response, "html.parser")
        server_link = soup.select_one("iframe")
        if server_link:
            server_link = server_link["src"]
            servers_link.append(server_link)
    # die(servers_link=servers_link,episode_link=episode_link)
    return servers_link


if __name__ == "__main__":
    search_term = "the 100"
    result = get_search_results_link(search_term)
    die(result)
    # link = "https://web.topcinema.cam/%d9%85%d8%b3%d9%84%d8%b3%d9%84-the-vampire-diaries-%d8%a7%d9%84%d9%85%d9%88%d8%b3%d9%85-%d8%a7%d9%84%d8%b3%d8%a7%d8%af%d8%b3-%d8%a7%d9%84%d8%ad%d9%84%d9%82%d8%a9-1-%d9%85%d8%aa%d8%b1%d8%ac%d9%85%d8%a9/"
    # die(get_episodes_list(link))
    # episode_link = "https://web.topcinema.cam/%d9%85%d8%b3%d9%84%d8%b3%d9%84-the-vampire-diaries-%d8%a7%d9%84%d9%85%d9%88%d8%b3%d9%85-%d8%a7%d9%84%d8%b3%d8%a7%d8%af%d8%b3-%d8%a7%d9%84%d8%ad%d9%84%d9%82%d8%a9-1-%d9%85%d8%aa%d8%b1%d8%ac%d9%85%d8%a9/watch/"
    # die(get_all_episodes_server_link(episode_link))
