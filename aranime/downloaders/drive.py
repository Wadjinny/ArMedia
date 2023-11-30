import re
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from aranime.utils.file_downloader import download_file
from aranime.utils import die


filter_function = lambda x: "drive.google.com" in x
priority = 13



def download(server_link, output_dir, file_name, desc=None,return_url=False):
    def get_id(link):
        if "export=download" in link:
            return re.findall(r"id=(.*)", link)[0]
        else:
            return re.findall(r"/d/(.*?)/", link)[0]

    id = get_id(server_link)
    url = f"https://drive.google.com/uc?id={id}&export=download"
    session = requests.Session()
    response = session.get(url)
    response = response.text 
    soup = BeautifulSoup(response, "html.parser")
    download_url = soup.select_one("form", id="download-form")
    if download_url:
        download_url = download_url["action"]
    else:
        return False
    response = session.head(download_url)
    download_url = response.headers["Location"]
    if return_url:
        return download_url
    return download_file(download_url, output_dir, file_name, desc=desc)
    
    
if __name__ == "__main__":
    server_link = "https://drive.google.com/file/d/1EzbVC-6O5XhTELRYsVrC4X5D-ivJxKDC/preview"
    output_dir = Path(".")
    file_name = "test.mp4"
    die(download_file(server_link, output_dir, file_name))

