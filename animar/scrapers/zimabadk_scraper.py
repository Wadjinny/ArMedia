import requests
import base64
import re
from urllib.parse import quote
from bs4 import BeautifulSoup
from pprint import pprint
from animar.utils import debug, die
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
            ).group(1)
            headers = {
                "cookie": "XSRF-TOKEN=eyJpdiI6IjMrODBCRXd6SXVzbzY5RXRsUWMzbVE9PSIsInZhbHVlIjoiYmRBRnJwMmFOc01JSDlVU3JhNHR1OFFtNHpzdDNxV2xkRmdGNVdqOVU5N2Q3TG91T0ROaUk4KzNWaDZXSWpJeFVIdE0zRG9NMkx2NnFZajVjYXBObFFBSnNNb1k4cUg0cXU4aGJqYkJpTWk3WjJKZWR0V21BZm5NTm9jU1lFdzYiLCJtYWMiOiI1OGJkYWU0ODQ4NWQwY2U5MjdlODE2YTkyMWU1MjU4YzVjZDg3NjI1M2VlYWM2MTljOTY2YzlmZGJiMjY5M2RiIiwidGFnIjoiIn0%253D; megamax_session=eyJpdiI6IlhJc3NzbTNIRFhIR3JqbDI0U2dPMVE9PSIsInZhbHVlIjoidEtpTkVGMXhReXRVSVZ4KzRmN091cEpIeVdSUmY3SXFwaUtoV2w0bmwwUWtmMm9ibzZwQnFUTXNOYUN1R0E4SUVIRnZmZStpK0QyL2tLdXhBaHpLaUNBZkN0SEpYSHFHVkNPYUoraStPK2s1YVJxT2pNa1BqUHR0bUFzSTdjeVoiLCJtYWMiOiJkM2YyYmNhYjUxN2I0Y2Y0YjhmNTI5NjNjODNmMjRjMTcwMDU5ZTlmMGUzZGFkMTc5NmQzYjU4YWJlNDEyMTQ3IiwidGFnIjoiIn0%253D",
                "x-inertia": "true",
                "x-inertia-partial-component": "web/files/mirror/video",
                "x-inertia-partial-data": "streams",
                "x-inertia-version": version,
            }
            response = requests.request("GET", link, headers=headers)
            path = "@.props.streams.data[].mirrors[].link"
            megamax_servers = jmespath.search(path, response.json())

            for i, s in enumerate(megamax_servers):
                if s.startswith("//"):
                    megamax_servers[i] = "https:" + s
            server_links.extend(megamax_servers)

    return server_links + download_link


# import requests

# url = "https://megamax.me/iframe/Ox3DAPel7nGiF"
# headers = {
#     "cookie": "XSRF-TOKEN=eyJpdiI6IjMrODBCRXd6SXVzbzY5RXRsUWMzbVE9PSIsInZhbHVlIjoiYmRBRnJwMmFOc01JSDlVU3JhNHR1OFFtNHpzdDNxV2xkRmdGNVdqOVU5N2Q3TG91T0ROaUk4KzNWaDZXSWpJeFVIdE0zRG9NMkx2NnFZajVjYXBObFFBSnNNb1k4cUg0cXU4aGJqYkJpTWk3WjJKZWR0V21BZm5NTm9jU1lFdzYiLCJtYWMiOiI1OGJkYWU0ODQ4NWQwY2U5MjdlODE2YTkyMWU1MjU4YzVjZDg3NjI1M2VlYWM2MTljOTY2YzlmZGJiMjY5M2RiIiwidGFnIjoiIn0%253D; megamax_session=eyJpdiI6IlhJc3NzbTNIRFhIR3JqbDI0U2dPMVE9PSIsInZhbHVlIjoidEtpTkVGMXhReXRVSVZ4KzRmN091cEpIeVdSUmY3SXFwaUtoV2w0bmwwUWtmMm9ibzZwQnFUTXNOYUN1R0E4SUVIRnZmZStpK0QyL2tLdXhBaHpLaUNBZkN0SEpYSHFHVkNPYUoraStPK2s1YVJxT2pNa1BqUHR0bUFzSTdjeVoiLCJtYWMiOiJkM2YyYmNhYjUxN2I0Y2Y0YjhmNTI5NjNjODNmMjRjMTcwMDU5ZTlmMGUzZGFkMTc5NmQzYjU4YWJlNDEyMTQ3IiwidGFnIjoiIn0%253D",
#     "x-inertia": "true",
#     "x-inertia-partial-component": "web/files/mirror/video",
#     "x-inertia-partial-data": "streams",
#     "x-inertia-version": "5a8caffbb01312d891cb5572a111f293"
# }

# response = requests.request("GET", url, headers=headers)

# print(response.text)

# get_all_episodes_server_link("https://www.zimabadk.com/yurei-deco-الحلقة-1/")

if __name__=="__main__":
    print(get_episodes_list("https://www.zimabadk.com/anime/migi-to-dali/"))
