import requests
import base64
import re
from urllib.parse import quote
from bs4 import BeautifulSoup
from armedia.utils import debug, die


arab_map = {
    "الموسم": "season",
    "الحلقة": "episode",
    "الاول": "1",
    "الثاني": "2",
    "الثالث": "3",
    "الرابع": "4",
    "الخامس": "5",
    "السادس": "6",
    "السابع": "7",
    "الثامن": "8",
    "التاسع": "9",
    "العاشر": "10",
    "الحادي عشر": "11",
    "الثاني عشر": "12",
    "الثالث عشر": "13",
    "الرابع عشر": "14",
    "الخامس عشر": "15",
    "السادس عشر": "16",
    "السابع عشر": "17",
    "الثامن عشر": "18",
    "التاسع عشر": "19",
    "العشرون": "20",
    "الحادي و العشرون": "21",
    "الثاني والعشرون": "22",
    "الثالث والعشرون": "23",
    "الرابع والعشرون": "24",
    "الخامس والعشرون": "25",
}


def translate_arabic_to_english(text: str) -> str:
    for ar_w, tr in reversed(arab_map.items()):
        text = text.replace(ar_w, tr)
    return text


def get_search_results_link(search_term: str) -> list[dict[str, str]]:
    search_term = quote(search_term)
    url = f"https://ak.sv/search?q={search_term}"
    response = requests.request("GET", url, timeout=100)
    response = response.text
    soup: BeautifulSoup = BeautifulSoup(response, "html.parser")
    medias = soup.select(
        "div.page.page-search > div.container > div.widget > div > div"
    )
    formated_medias = []
    for media in medias:
        link = media.select_one("a")["href"]
        name = media.select_one("a.text-white").text
        name = translate_arabic_to_english(name)
        name = re.sub(r"\s+", " ", name)
        name = re.sub(r"[^\x00-\x7f]", r"", name).strip()

        formated_medias.append({"name": name, "link": link})
    return formated_medias[::-1]


def get_episodes_list(media_link) -> list[str]:
    if "/movie/" in media_link:
        return [{"link": media_link, "number": "1"}]
    response = requests.request("GET", media_link, timeout=100)
    response = response.content.decode("utf-8")
    soup = BeautifulSoup(response, "html.parser")
    episodes = soup.select("#series-episodes > div.widget-body > div > div")
    episodes_info = []
    for episode in episodes:
        link = episode.select_one("a")["href"]
        number = episode.select_one("a").text
        number = re.sub(r"[^0-9]", "", number)
        episodes_info.append({"link": link, "number": number})
    return episodes_info[::-1]


def get_all_episodes_server_link(episode_link):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        "cookie": """
        akwamVerification3 = eyJpdiI6Ik11QU1RV2VNOGVnS0Jlc1FRV2NtbXc9PSIsInZhbHVlIjoibFR1NlpNSDROcjZta3c1Q2Q5V1VmQT09IiwibWFjIjoiODE2MzYwODUwZDcyMjRlYmY3ZDc4NWFhNTgzYzkyMjI1M2M4MTE3YjFjNmQ3MzM2OTMyOTA5ZDNmNmJmOThiNSJ9;
        XSRF-TOKEN = eyJpdiI6InpLMmU5ZVwvQ1ZjMlA5elBzZ1V4THNBPT0iLCJ2YWx1ZSI6IkpcL08reXlJaVBYMThnT3ZPKzY0alBnMmRKMUZjM1U1QU5iT1dTQkkwM0ZxYStEelRESFhHQVRib0xRRkhQXC8ySiIsIm1hYyI6ImE2ZDg4NjcxMjI5ZmNlMWUwYzI3NzI1MWQ4NmQ4ZjM5YWFmZWE2YjNkZmVhZGFjNmU2ZTkzMDVhNGZiYTUxZTQifQ%3D%3D;
        akwam_session = eyJpdiI6IjA0bmZzMzd4bVhySHQxQm5BMU5vMEE9PSIsInZhbHVlIjoiTzQybW93ME5pRkhyMVZDTnFzNmlFbFR1V0VrVEFQbldhZHBGRytzQnV2NXBpdFwvYTNVYll5QndLSmRRQ1FkN1kiLCJtYWMiOiI3NWZiYWNiNGM4MGU4ZjZiNDZmODZmMWZmNzA3NDM3ODNkNGYxZGYxMTA3NzNmMWE3YjE5ZjcxNjM5MWIyNDhiIn0%3D;
        qqvxl11JK6q52al0etnCb8JHnJ5mYjU2CjPmPpfP = eyJpdiI6IjN1aXZCVlRqaTdkcG5KS0xhYjQ1VXc9PSIsInZhbHVlIjoiRWlGRk5ETk0xclJLd0J4Z29YTjFUK0dwZFRYaFY1T0thdWh1QWlaQm9HdHI4QXRLbWxPKzZYZksxNkZLU2JkckZ6WVJCN0I5RjNSSktYRmFxbzRkZjhweXNwY09aUTlsSVViRklNcUFjaWtmeGJ2bTd2KzRsa1pwOHdBQnFKVkZXbUtHU0xZWnhuYUFJMHhsNEY0QnJsS1MzYnE1TEdoRExqb1RqallQbGVXbVpuY1hWVHVwMElIQnk5M29qSVFmaGN4eTVQT0tSR3ZMK25tWlF6MG9SeGIxZVMwVjR5RUNDXC9rbXYyU2tWc1wvQ0wzK25FVU85K21jR0RpZ2Y1MWh6dGh3ZGlXS2dtOGVWblc0UlFNalA1U1oyNTNrdkNrN2tZVGdPK3E3a1wvZXVNeWppeTNheGEyczlMYTUyZGNMZGg1QU5NNGFzbFI1YjFkOHFONlV2QWlqRmg3U0FoSko5NXRwdzN2UU9kbWdkNHh2NXoyUGNBSmZmTkxPRVwvTXJjb3JZMmVcL0xiUjlpbjRcL0FNaURcL0VPV2lHN3FkTGJQaDJUYmNZK0hjelwvRzFKQnhRV3pRT3hsUmkwY3RGR3dyK2NaIiwibWFjIjoiOTcyZGFmYThlMmU2OTc5MGYzNTE2ZjQyZmUwZjVkOWUyMjI5MjY4OWFlOTNmOWViZGJhMjA3ZjBjNzhjYzNmOSJ9""".replace(
            "\n", ""
        ).replace(
            " ", ""
        ),
    }
    session = requests.Session()
    session.headers.update(headers)
    response = session.request("GET", episode_link, timeout=100)
    response = response.text
    # <a href="http://noon.khsm.io/watch/89859"
    episode_id = re.findall(r"ak.sv/[a-z]+/(\d+/.*)", episode_link)[0]
    server_id = re.findall(r"http://noon.khsm.io/watch/(\d+)", response)
    if server_id:
        server_id = server_id[0]
    else:
        return []
    # https://ak.sv/watch/157456/84659/%D8%B1%D9%88%D8%B2-%D9%88%D9%84%D9%8A%D9%84%D9%89/%D8%A7%D9%84%D8%AD%D9%84%D9%82%D8%A9-8
    url = f"https://ak.sv/watch/{server_id}/{episode_id}"
    response = session.request("GET", url, timeout=100)
    response = response.text
    links = re.findall(r'"(https://.*?/download/.*?\.mp4)"', response)

    download_links = url.replace("watch", "download")
    response = session.request("GET", download_links, timeout=100)
    response = response.text

    download_links = re.findall(r'"(https://.*?/download/.*?\.mp4)"', response)
    download_links.extend(links)
    return download_links


if __name__ == "__main__":
    # search_term = "family guy"
    # result = get_search_results_link(search_term)
    # die(result)
    # link = "https://ak.sv/series/2628/family-guy-%D8%A7%D9%84%D9%85%D9%88%D8%B3%D9%85-%D8%A7%D9%84%D8%AD%D8%A7%D8%AF%D9%8A-%D8%B9%D8%B4%D8%B1-4"
    # die(get_episodes_list(link))
    episode_link = "https://ak.sv/episode/84659/%D8%B1%D9%88%D8%B2-%D9%88%D9%84%D9%8A%D9%84%D9%89/%D8%A7%D9%84%D8%AD%D9%84%D9%82%D8%A9-8"
    die(get_all_episodes_server_link(episode_link))
