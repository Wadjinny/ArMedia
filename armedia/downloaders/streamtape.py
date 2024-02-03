import re
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from armedia.utils.file_downloader import download_file
from armedia.utils import die,debug
from urllib.parse import urlencode

filter_function = lambda x: "streamtape" in x
priority = 10

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "fr,en-US;q=0.9,en;q=0.8",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "sec-ch-ua": "\"Not A(Brand\";v=\"99\", \"Google Chrome\";v=\"121\", \"Chromium\";v=\"121\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Linux\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    # "cookie": "_b=kube13; _csrf=d6f020ceb3e12061af7fec17bdfd00b63ade8b770ced4b29f37b7ce9bef3fe57a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22dvQ2kzNI23DhnbPObdzpz00--ldht7u0%22%3B%7D"
}

def download(server_link, output_dir, file_name, desc=None, return_url=False):
    session = requests.Session()
    session.headers.update(headers)
    response = session.request("GET", server_link, timeout=100)
    response = response.text

    tokens = re.findall(r"&(token=.+)'", response)
    token = tokens[-1]
    ids = re.findall(r"get_video\?(id=.+&expires=.+&ip=.+)&token", response)
    id=ids[0]
    
    full_url =f"https://streamtape.cc/get_video?{id}&{token}&stream=1"
    if return_url:
        return full_url
    
    return download_file(url=full_url, output_dir=output_dir, file_name=file_name, desc=desc)
        


if __name__ == "__main__":
    server_link = "https://streamtape.cc/e/Gvl4Z3JlyXFAmY"
    output_dir = Path(".")
    file_name = "test.mp4"
    die(download(server_link, output_dir, file_name))
