import requests
import base64
import re
from urllib.parse import quote
from bs4 import BeautifulSoup
from armedia.utils import debug, die
import json
from pathlib import Path

site_extension = "cyou"

def decode_link(encoded_url):
    # Replace URL-safe characters
    fixed_url = encoded_url.replace('-', '+').replace('_', '/').replace(',', '=')
    
    # Add padding if necessary
    padding = len(fixed_url) % 4
    if padding:
        fixed_url += '=' * (4 - padding)
    
    # Decode with base64
    return base64.b64decode(fixed_url).decode('utf-8')

def decode_episode_data(encoded_data):
    # Split the encoded data
    parts = encoded_data.split('.')
    
    # Decode from base64
    encrypted_data = base64.b64decode(parts[0])
    key = base64.b64decode(parts[1])
    
    # XOR decryption using the key
    decoded_data = ''
    for i in range(len(encrypted_data)):
        decoded_char = encrypted_data[i] ^ key[i % len(key)]
        decoded_data += chr(decoded_char)
    
    # Parse and return JSON data
    return json.loads(decoded_data)

def get_final_url(sp, sx, server_id=0, api_key="73503d58-f228-425f-97f1-2d9512f5772c"):
    encoded_url = sp[server_id]
    decoding_data = sx[server_id]
    
    # Get chars to remove and decode URL
    decoded_key = base64.b64decode(decoding_data["k"]).decode('utf-8')
    chars_to_remove = decoding_data["d"][int(decoded_key)]
    video_url = base64.b64decode(encoded_url).decode('utf-8')[:-chars_to_remove]
    
    # Check if Yonaplay URL and append API key if needed
    yonaplay_pattern = r'^https://yonaplay\.org/embed\.php\?id=\d+$'
    return f"{video_url}&apiKey={api_key}" if re.match(yonaplay_pattern, video_url) else video_url

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
    # encoded ep data: var processedEpisodeData = 'axdgIh0...'
    encoded_ep_data = re.search(r"var\s+processedEpisodeData\s*=\s*'([^']+)'", response).group(1)
    episodes_info = decode_episode_data(encoded_ep_data)
    res_episodes_info = []
    for episode in episodes_info:
        res_episodes_info.append({"link": episode["url"], "number": episode["number"]})
    return res_episodes_info


def get_all_episodes_server_link(episode_link):
    headers = {'referer': f'https://witanime.{site_extension}/','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',}
    response = requests.request("GET", episode_link, headers=headers)
    response = response.text
    # get sp: var sP = ["aH..."];
    sp = re.search(r"var\s+sP\s*=\s*(\[.*?\]);", response).group(1)
    # get sx: var sX = [{"d":[10,86,79,74,10,15,89,88,98,34],"k":"NA=="},{"d":[39,97,19,77,49,10,54,19,26,22],"k":"NQ=="}];
    sx = re.search(r"var\s+sX\s*=\s*(\[.*?\]);", response).group(1)
    sp = json.loads(sp)
    sx = json.loads(sx)
    servers_res = []
    for server_id in range(len(sp)):
        final_url = get_final_url(sp, sx, server_id)
        print(final_url)
        if "yonaplay" in final_url:
            response = requests.request("GET", final_url, headers=headers)
            # get server link 
            # go_to_player('')
            server_link = re.search(r"go_to_player\('(.*?)'\)", response.text).group(1)
            server_link = decode_link(server_link)
            # die(server_link=server_link)
            if "soraplay" in server_link:
                response = requests.request("GET", server_link, headers=headers)
                response = response.text
                server_links = re.findall(r'"file":"(.*?)","ty', response)[0]
                servers_res.append(server_links)
            else:
                servers_res.append(server_link)
        elif "playerwish" in final_url:
            pass
        else:
            servers_res.append(final_url)
    return servers_res
    




if __name__ == "__main__":
    # print(
    #     get_episodes_list(
    #         "https://witanime.cyou/anime/itsudatte-bokura-no-koi-wa-10-cm-datta/"
    #     )
    # )
    # test_decode_data = "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.MGxCTGhIRjNrUFI1QUxZWmEzZkhoRThObVp0YzBXbEw="

    # print(decode_episode_data(test_decode_data))

    episode_link = "https://witanime.cyou/episode/boruto-naruto-next-generations-%d8%a7%d9%84%d8%ad%d9%84%d9%82%d8%a9-278/"
    print(get_all_episodes_server_link(episode_link))
