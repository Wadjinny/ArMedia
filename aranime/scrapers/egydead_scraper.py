import requests
import re
from bs4 import BeautifulSoup
from aranime.utils import debug, die
from urllib.parse import urlencode
import jmespath
import cloudscraper


scraper = cloudscraper.create_scraper(browser="chrome")


headers = {
    "cookie": "I.U3xOajT.vuGWRQLNC1K3RzEr.3geZReVXlx4r1EBw-1701376979-0-1-2338f809.62f14f57.578f7038-150.0.0",
    # "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "x-requested-with": "XMLHttpRequest",
}


def get_search_results_link(search_term: str) -> list[str]:
    url = "https://egydead.space/wp-content/themes/egydeadc-taq/Ajax/live-search.php"
    payload = "search=" + search_term
    response = scraper.post(url, data=payload, headers=headers)
    response = response.text
    soup = BeautifulSoup(response, "html.parser")
    anime_list = soup.select(".liveItem")
    result = []
    for anime in anime_list:
        name = anime.select_one("h3").text
        name = re.sub(r"[^\x00-\x7f]", r"", name)
        name = name.strip().lstrip().rstrip()
        link = anime.select_one("a")["href"]
        result.append({"name": name, "link": link})
    return result


def get_episodes_list(anime_link) -> list[str]:
    headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    # "accept-language": "fr,en-US;q=0.9,en;q=0.8",
    # "cache-control": "no-cache",
    # "content-type": "application/x-www-form-urlencoded",
    # "pragma": "no-cache",
    "sec-ch-ua": "\"Google Chrome\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
    # "sec-ch-ua-mobile": "?0",
    # "sec-ch-ua-platform": "\"Linux\"",
    # "sec-fetch-dest": "document",
    # "sec-fetch-mode": "navigate",
    # "sec-fetch-site": "same-origin",
    # "upgrade-insecure-requests": "1",
    "cookie": "cf_chl_2=51476c5ec104449",
    # "Referer": "https://egydead.space/serie/%D8%AC%D9%85%D9%8A%D8%B9-%D9%85%D9%88%D8%A7%D8%B3%D9%85-%D9%88%D9%82%D8%AA-%D8%A7%D9%84%D9%85%D8%BA%D8%A7%D9%85%D8%B1%D8%A9-adventure-time-%D9%85%D8%AA%D8%B1%D8%AC%D9%85-%D9%83%D8%A7%D9%85%D9%84/?__cf_chl_tk=Ro0x5BSAlKNx3xKypxNbxyV5fvoDi1.1fThhW2PFZNg-1701377577-0-gaNycGzNC2U",
    # "Referrer-Policy": "same-origin"
    }


    response = scraper.get(anime_link, timeout=100, headers=headers)
    response = response.text
    die(response)
    soup = BeautifulSoup(response, "html.parser")
    episode_list_el = soup.select(".EpsList a")

    episodes = []
    for ep in episode_list_el[::-1]:
        number = ep.text
        number = re.sub(r"[^\x00-\x7f]", r"", number)
        number = number.strip().lstrip().rstrip()
        link = ep["href"]
        episodes.append({"number": number, "link": link})

    return episodes


def get_all_episodes_server_link(episode_link):
    payload = "View=1"
    response = scraper.post(episode_link, data=payload, headers=headers)
    die(response.text)
    soup = BeautifulSoup(response.text, "html.parser")
    server_list = soup.select(".serversList li")
    server_list = [s["data-link"] for s in server_list]
    return server_list



if __name__ == "__main__":
    search_term = "adventure time"
    series_link = "https://egydead.space/season/%d9%85%d8%b3%d9%84%d8%b3%d9%84-adventure-time-fionna-and-cake-2023-%d9%85%d8%aa%d8%b1%d8%ac%d9%85-%d9%83%d8%a7%d9%85%d9%84/"
    episode_link = "https://egydead.space/episode/%D9%85%D8%B3%D9%84%D8%B3%D9%84-adventure-time-fionna-and-cake-%D8%A7%D9%84%D8%AD%D9%84%D9%82%D8%A9-1-%D9%85%D8%AA%D8%B1%D8%AC%D9%85%D8%A9/"

    # print(get_all_episodes_server_link(episode_link))
    print(get_episodes_list(series_link))
