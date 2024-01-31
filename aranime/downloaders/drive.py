import re
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from aranime.utils.file_downloader import download_file
from aranime.utils import die,debug
from urllib.parse import urlencode

filter_function = lambda x: "drive.google.com" in x
priority = 10

headers = {
    "cookie": (
        "__Secure-3PSID=fgh4UlbqWUxTLODfiRQnb1MdrvGA4PsON3zYV9uYsBeAueUMkXFmaROnLDWOgwbRDl5YiA.;"
        "__Secure-3PSIDTS=sidts-CjIBPVxjSrRdxPSH6EIHOeca02Vqi5zD9R7LcJqa8Zn68WuaNseIcUlPPNldhF8p9WE5rBAA;"
        "__Secure-3PSIDCC=ABTWhQGRUToVHgvbg74TC4d4ooMfZOgaHgyw-h4tnzk0KtSej80zE258IjzgAERZ4hYhfpFAnoo"
    ),
}


def download(server_link, output_dir, file_name, desc=None, return_url=False):
    def get_id(link):
        if "export=download" in link:
            return re.findall(r"id=(.*)", link)[0]
        else:
            return re.findall(r"/d/(.*?)/", link)[0]

    id = get_id(server_link)
    url = f"https://drive.usercontent.google.com/download?id={id}&export=download"
    session = requests.Session()
    session.headers.update(headers)
    response = session.get(url)
    response = response.text
    soup = BeautifulSoup(response, "html.parser")
    download_form = soup.select_one("form", id="download-form")
    if download_form:
        download_base = download_form["action"]
        download_params = download_form.select("input")
        # die(download_params)
        download_params = {
            x["name"]: x["value"] for x in download_params if x.get("name")
        }
        if download_params.get("at") is None:
            debug("[at] param not found in Drive url")
            return False
        download_url = download_base + "?" + urlencode(download_params)
    else:
        return False
    if return_url:
        return download_url
    return download_file(
        download_url, output_dir, file_name, desc=desc, CONNECTIONS=1, session=session
    )


if __name__ == "__main__":
    server_link = "https://drive.usercontent.google.com/download?id=1B8aF0FLYOct3aOVhI_jdi8uoLz4CyFPc&export=download&authuser=0"
    output_dir = Path(".")
    file_name = "test.mp4"
    die(download(server_link, output_dir, file_name))
