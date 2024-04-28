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
    md5 = re.findall(r"(/pass_md5/.*?)',", response)
    token = re.findall(r"\?token=.*?&expiry=", response)
    if not md5 or not token:
        return False
    url = f"https://d0000d.com{md5[0]}"
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

    base_url = response.text
    full_url = f"{base_url}IrHklgWrek{token[0]}{datetime.now().timestamp()*1000:.0f}"
    try:
        response = session.request("HEAD", full_url, headers=headers, timeout=100)
    except requests.exceptions.RequestException as e:
        return False
    if return_url:
        return full_url
    session.headers.update(headers)
    return download_file(
        full_url, output_dir=output_dir, file_name=file_name, desc=desc, session=session
    )


if __name__ == "__main__":
    server_link = "https://d000d.com/e/q9hysf878jcl"
    output_dir = Path(".")
    file_name = "test.mp4"
    die(download(server_link, output_dir, file_name))
