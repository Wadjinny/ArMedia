import re
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from armedia.utils.file_downloader import download_file
from armedia.utils import die, debug
from urllib.parse import urlencode
from datetime import datetime

filter_function = lambda x: "d0o0d" in x
priority = 10

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "fr,en-US;q=0.9,en;q=0.8",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
}


def download(server_link, output_dir, file_name, desc=None, return_url=False):
    global headers
    session = requests.Session()
    session.headers.update(headers)
    response = session.request("GET", server_link, timeout=100)
    response = response.text
    # $.get('/pass_md5/103682933-85-170-1706983115-9ba8aa2fd2fbacd411ce2b6460bf739f/18uk7y70cfhuw12grfhrko9v',
    md5 = re.findall(r"(/pass_md5/.*?)',", response)
    token = re.findall(r"\?token=.*?&expiry=", response)
    if not md5 or not token:
        return False
    # debug(md5=md5, token=token)
    url = f"https://d0000d.com/{md5[0]}"
    headers = {
        "accept": "*/*",
        "accept-language": "fr,en-US;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest",
        "cookie": "lang=1",
        "Referer": "https://d0000d.com/e/",
        "Referrer-Policy": "strict-origin-when-cross-origin",
    }
    response = session.request("GET", url, headers=headers, timeout=100)
    # https://op168li.video-delivery.net/u5kj2cd5e3elsdgge4cteoyckchpcwe4klb7mwp55gikzpkaz7gq3ad45tbq/6npvqqwn0b~

    base_url = response.text
    full_url = f"{base_url}IrHklgWrek{token[0]}{datetime.now().timestamp()*1000:.0f}"
    response = session.request("HEAD", full_url, headers=headers, timeout=100)
    if return_url:
        return full_url
    session.headers.update(headers)
    return download_file(full_url, output_dir=output_dir, file_name=file_name, desc=desc,session=session)


if __name__ == "__main__":
    server_link = "https://d0o0d.com/e/mtxij6jgkp9s"
    output_dir = Path(".")
    file_name = "test.mp4"
    die(download(server_link, output_dir, file_name))
