import re
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from armedia.utils.file_downloader import download_file
from armedia.utils import die, debug
from urllib.parse import urlencode
import json

app_dir = Path().home() / ".armedia"
config_file = app_dir / "config.json"
config = json.load(config_file.open())

filter_function = lambda x: "drive.google.com" in x
priority = 10

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "fr,en-US;q=0.9,en;q=0.8",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    "sec-ch-ua-arch": '"x86"',
    "sec-ch-ua-bitness": '"64"',
    "sec-ch-ua-full-version": '"121.0.6167.85"',
    "sec-ch-ua-full-version-list": '"Not A(Brand";v="99.0.0.0", "Google Chrome";v="121.0.6167.85", "Chromium";v="121.0.6167.85"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-model": '""',
    "sec-ch-ua-platform": '"Linux"',
    "sec-ch-ua-platform-version": '"6.5.0"',
    "sec-ch-ua-wow64": "?0",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "cross-site",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
}

headers.update(config.get("drive_headers", {}))


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

    if session.head(url).headers.get("Content-Type") == "application/octet-stream":
        if return_url:
            return url
        return download_file(
            url, output_dir, file_name, desc=desc, CONNECTIONS=1, session=session
        )

    response = session.get(url, timeout=100)
    response = response.text
    soup = BeautifulSoup(response, "html.parser")
    download_form = soup.select_one("form", id="download-form")
    if download_form:
        download_base = download_form["action"]
        download_params = download_form.select("input")
        download_params = {
            x["name"]: x["value"] for x in download_params if x.get("name")
        }
        download_url = download_base + "?" + urlencode(download_params)
    else:
        return False
    if return_url:
        return download_url
    return download_file(
        download_url, output_dir, file_name, desc=desc, CONNECTIONS=1, session=session
    )


if __name__ == "__main__":
    server_link = "https://drive.google.com/uc?id=1ByR9C_Q1lFRvQnoFcRY2htW4kURDbq57&export=download"
    output_dir = Path(".")
    file_name = "test.mp4"
    die(download(server_link, output_dir, file_name))
