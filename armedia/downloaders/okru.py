# %%
import requests
from bs4 import BeautifulSoup
import json
from armedia.utils.file_downloader import download_file

# %%

filter_function = lambda x: "ok.ru" in x
priority = 5

def download(server_link, output_dir, file_name, desc=None,return_url=False):
    session = requests.Session()
    response = session.get(server_link)
    response = response.text

    try:
        soup = BeautifulSoup(response, "html.parser")
        data = soup.find("div", {"data-module": "OKVideo"})
        data = data["data-options"]
        data = json.loads(data)

        video_links = json.loads(data["flashvars"]["metadata"]).get("videos")
        video_links = [i["url"] for i in video_links][::-1]
    except (KeyError, TypeError):
        return False
    
    if return_url:
        return video_links[0]
    return download_file(video_links[0], output_dir, file_name, desc=desc)
