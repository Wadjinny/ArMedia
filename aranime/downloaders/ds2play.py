import requests
import re
from aranime.utils.file_downloader import download_file
from aranime.utils import die,debug
import cloudscraper
import random
from datetime import datetime
filter_function = lambda x: "ds2play.com" in x
priority = 10


def download(server_link, output_dir, file_name, desc=None, return_url=False):
    def gen_pass():
        char_set = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        return "".join(random.sample(char_set, 10))
    scraper = cloudscraper.create_scraper()
    response = scraper.get(server_link)
    response = response.text
    md5 = re.findall(r"(/pass_md5/.*?)',", response)[0]
    token = re.findall(r'"(\?token.*?=)"', response)[0]
    baseurl = "https://ds2play.com"
    url = baseurl + md5
    headers = {
        "Referer": "https://ds2play.com/",
    }
    pass_key = gen_pass()
    # in milliseconds
    expiry = int(datetime.now().timestamp() * 1000) + 200000
    response = scraper.get(url, headers=headers)
    url_first_part = response.text
    download_url = url_first_part+pass_key+token+str(expiry)
    session = requests.Session()
    session.headers.update(headers)
    if return_url:
        return download_url
    return download_file(download_url, output_dir, file_name, session=session, desc=desc)
    
    


if __name__ == "__main__":
    url = "https://ds2play.com/e/8ge1hg1bjt1r"
    download(url, "test", "test.mp4")
