import requests
import re
from aranime.utils.file_downloader import download_file


filter_function = lambda x: "uploadourvideo.com" in x
priority = 10

def download(server_link, output_dir, file_name, desc=None,return_url=False):
    session = requests.Session()
    server_link = server_link.replace("watch", "embed")
    session = requests.Session()
    response = session.get(server_link)
    response = response.text
    mp4_url = re.findall(r'file: "(.*?)"', response)
    if mp4_url:
        mp4_url = mp4_url[0]
    else:
        return False
    if return_url:
        return mp4_url
    return download_file(mp4_url, output_dir, file_name, desc=desc)


# upload_links = list(filter(lambda x: "uploadourvideo.com" in x, server_links))
