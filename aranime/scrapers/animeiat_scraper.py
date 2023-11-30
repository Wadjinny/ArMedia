import requests
import base64
import re
from urllib.parse import quote
from bs4 import BeautifulSoup
from pprint import pprint
from aranime.utils import debug, die
from urllib.parse import urlencode
import jmespath


def get_search_results_link(search_term: str) -> list[dict[str, str]]:
    params = {"q": search_term}
    url = f"https://www.animeiat.xyz/search?{urlencode(params)}"
    session = requests.Session()
    response = session.get(url, timeout=100)
    response = response.text
    soup = BeautifulSoup(response, "html.parser")
    anime_list = soup.select(".search-results .row > div")
    
    result_animes = []
    base_url = "https://www.animeiat.xyz"
    for anime in anime_list:
        name = anime.select_one(".anime-title.text-center a h2").text
        link = anime.select_one(".anime-title.text-center a")["href"]
        result_animes.append({"name": name, 
                              "link": base_url + link
                              })
    return result_animes

def get_episodes_list(anime_link) -> list[str]:
    session = requests.Session()
    response = session.get(anime_link, timeout=100)
    response = response.text
    soup = BeautifulSoup(response, "html.parser")
    episodes = soup.select(".anime-episodes .row > div")
    result_episodes = []
    base_url = "https://www.animeiat.xyz"
    for episode in episodes:
        link = episode.select_one(".v-responsive__content a")["href"]
        number = episode.select_one(".v-responsive__content .v-chip__content").text
        number = re.sub(r"\D+", "", number)
        result_episodes.append({"link": base_url + link,
                                "number": number
                                })
    return result_episodes

def get_all_episodes_server_link(episode_link)->list[str]:
    session = requests.Session()
    response = session.get(episode_link, timeout=100)
    response = response.text
    soup = BeautifulSoup(response, "html.parser")
    form = soup.select_one("form[target='_blank']")
    action = form["action"]
    name = form.select_one("input").get("name")
    value = form.select_one("input").get("value")
    payload = {name: value}
    
    session.headers.update({"Referer": episode_link})
    response = session.post(action, data=payload)
    response = response.text
    soup = BeautifulSoup(response, "html.parser")
    another_form = soup.select_one("form#form[method='post']")
    if another_form:
        action = another_form["action"]
        name = another_form.select_one("input").get("name")
        value = another_form.select_one("input").get("value")
        payload = {name: value}
        session.headers.update({"Referer": action})
        response = session.post(action, data=payload)
        response = response.text
        soup = BeautifulSoup(response, "html.parser")
    
    iframe = soup.select_one("iframe")
    link = iframe["src"]
    
    session.headers.update({"Referer": link})
    response = session.get(link)
    response = response.text
    soup = BeautifulSoup(response, "html.parser")
    sources = soup.select("video > source")
    links = [source["src"] for source in sources]
    return links
    

if __name__ == "__main__":
    search_term = "astarotte"
    url = "https://www.animeiat.xyz/watch/boruto-naruto-next-generations-episode-1"
    
    get_all_episodes_server_link(url)