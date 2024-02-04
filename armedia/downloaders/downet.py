import re
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from armedia.utils.file_downloader import download_file
from armedia.utils import die,debug
from urllib.parse import urlencode

filter_function = lambda x: "downet.net" in x
priority = 10

headers={
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "sec-ch-ua": "\"Not A(Brand\";v=\"99\", \"Google Chrome\";v=\"121\", \"Chromium\";v=\"121\"",
    "sec-ch-ua-arch": "\"x86\"",
    "sec-ch-ua-bitness": "\"64\"",
    "sec-ch-ua-full-version": "\"121.0.6167.85\"",
    "sec-ch-ua-full-version-list": "\"Not A(Brand\";v=\"99.0.0.0\", \"Google Chrome\";v=\"121.0.6167.85\", \"Chromium\";v=\"121.0.6167.85\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-model": "\"\"",
    "sec-ch-ua-platform": "\"Linux\"",
    "sec-ch-ua-platform-version": "\"6.5.0\"",
    "sec-ch-ua-wow64": "?0",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
}


def download(server_link, output_dir, file_name, desc=None, return_url=False):
    if return_url:
        return server_link
    return download_file(server_link, output_dir, file_name, desc=desc,CONNECTIONS=1)

if __name__ == "__main__":
    server_link = "https://s216d1.downet.net/download/1707152401/65bfc291ada5c/Rose.Wa.Layla.S01E08.1080p.WEB-DL.AKWAM.mp4"
    output_dir = Path(".")
    file_name = "test.mp4"
    die(download(server_link, output_dir, file_name))
