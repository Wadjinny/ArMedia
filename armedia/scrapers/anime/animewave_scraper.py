import requests
from bs4 import BeautifulSoup
import re
from armedia.utils import die


def search_media(search_term):
    querystring = {"keyword": search_term}
    headers = {
        "cookie": "waf_jschallenge_7a997c1d70ce9f68=1700772494-6e657673a79c619511e9aa69e95baae8",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    }
    url = "https://aniwave.to/filter"
    response = requests.request("GET", url, headers=headers, params=querystring)
    html_doc = response.text
    soup = BeautifulSoup(html_doc, "html.parser")
    anime_list = soup.select("#list-items > div")

    anime_list_formated = []
    for anime in anime_list:
        english_name = anime.select_one(".name.d-title").text
        name: str = anime.select_one(".name.d-title")["data-jp"] or english_name
        name = re.sub(r"[^\x00-\x7f]", r" ", name)
        name = name.strip().lstrip()
        episode_count = anime.select_one(".ep-status.total")
        if episode_count:
            episode_count = int(episode_count.text)
        else:
            episode_count = 1
        anime_list_formated.append(
            {"name": name, "english_name": english_name, "episode_count": episode_count}
        )
    return anime_list_formated



if __name__ == "__main__":
    search_term = "fate"
    die(search_media(search_term))
