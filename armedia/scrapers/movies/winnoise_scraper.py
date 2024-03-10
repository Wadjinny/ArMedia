import requests
import base64
import re
from urllib.parse import quote
from bs4 import BeautifulSoup
from armedia.utils import debug, die

headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-requested-with": "XMLHttpRequest",
    "cookie": "show_share=true",
    "Referer": "https://winnoise.com/",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
}
session = requests.Session()


def get_search_results_link(search_term: str) -> list[dict[str, str]]:
    return []
    search_term = quote(search_term)
    url = "https://winnoise.com/ajax/search"
    body = f"keyword={search_term}"
    response = session.request("POST", url, headers=headers, data=body, timeout=100)
    response = response.text
    soup = BeautifulSoup(response, "html.parser")
    titles = soup.select(".nav-item")[:-1]
    titles_formated = []
    for title in titles:
        link = "https://winnoise.com" + title["href"]
        name = title.select_one("h3").text
        media_type = title.select_one("span:last-child").text
        id = re.search(r"-(\d+)$", link).group(1)
        if media_type == "TV":
            url = f"https://winnoise.com/ajax/season/list/{id}"
            response = session.request("GET", url, headers=headers, timeout=100)
            response = response.text
            soup = BeautifulSoup(response, "html.parser")
            seasons = soup.select(".dropdown-menu.dropdown-menu-new a")
            seasons = [
                {"name": season.text, "id": season["data-id"]} for season in seasons
            ]
            for season in seasons:
                titles_formated.append(
                    {
                        "name": f"{name} {season['name']}",
                        "id": season["id"],
                        "type": media_type,
                    }
                )
        else:
            titles_formated.append({"name": name, "id": id, "type": media_type})

    return titles_formated


def get_episodes_list(media_desc) -> list[str]:
    if media_desc["type"] == "Movie":
        return [{"id": media_desc["id"], "number": "1", "type": "Movie"}]
    id = media_desc["id"]
    url = f"https://winnoise.com/ajax/season/episodes/{id}"
    response = session.get(url, headers=headers, timeout=100)
    response = response.text
    soup = BeautifulSoup(response, "html.parser")
    episodes = soup.select("li a")
    episodes = [
        {"id": episode["data-id"], "number": episode["title"], "type": "TV"}
        for episode in episodes
    ]
    return episodes


rabbit_headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-requested-with": "XMLHttpRequest",
    "Referer": "https://rabbitstream.net/v2/embed-4",
    "user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Referrer-Policy": "strict-origin-when-cross-origin",
}


def get_all_episodes_server_link(episodes_desc):
    id = episodes_desc["id"]
    if episodes_desc["type"] == "Movie":
        url = f"https://winnoise.com/ajax/episode/list/{id}"
    else:
        url = f"https://winnoise.com/ajax/episode/servers/{id}"
    response = session.get(url, headers=headers, timeout=100)
    response = response.text
    server_ids = re.findall(r'data-linkid="(\d+)"', response)
    if not server_ids:
        server_ids = re.findall(r'data-id="(\d+)"', response)
    server_ids_stage2 = []
    for server_id in server_ids:
        url = f"https://winnoise.com/ajax/episode/sources/{server_id}"
        response = session.get(url, headers=headers)
        response = response.json()
        link = response["link"]
        if "rabbitstream" not in link:
            continue
        rabbit_id = re.findall(r"embed-\d+/(.+)\?", link)[0]
        rabbit_embed = re.findall(r".net(/.+/embed-\d+)/", link)[0]
        url = f"https://rabbitstream.net/ajax{rabbit_embed}/getSources?id={rabbit_id}&v=49138&h=e524adfb248218e77a2e84aebeb43fb9b425a2d0&b=1878522368"
        # die(url)
        response = session.get(url, headers=rabbit_headers)
        response = response.json()
        server_link = response["sources"]
        server_link = "https://rabbitstream.net/" + server_link
        die(server_link)
        captions = []
        for e in response["tracks"]:
            if e["kind"] == "captions":
                captions.append({"file": e["file"], "label": e["label"]})
        server_ids_stage2.append({"link": server_link, "captions": captions})
        
    return server_ids_stage2


if __name__ == "__main__":
    # search_term = "the 100"
    # result = get_search_results_link(search_term)
    # die(result)
    # media_desc =  {'name': 'The 100 Season 1', 'id': '9', 'type': 'TV'}
    # die(get_episodes_list(media_desc))
    episode_desc = {'id': '19467', 'number': 'Eps 1: Everything Is Great!', 'type': 'TV'}    
    die(get_all_episodes_server_link(episode_desc))
