import requests
import re
from pathlib import Path
from armedia.utils.file_downloader import download_file
from armedia.utils import die

filter_function = lambda x: "mediafire.com" in x
priority = 1
def download(server_link, output_dir, file_name, desc=None,return_url=False):
    def extractDownloadLink(contents):
        for line in contents.splitlines():
            m = re.search(r'href="((http|https)://download[^"]+)', line)
            if m:
                return m.groups()[0]
            
    session = requests.Session()
    response = session.get(server_link)
    content = response.text
    download_url = extractDownloadLink(content)
    if not download_url:
        return False
    if return_url:
        return download_url
    return download_file(download_url, output_dir, file_name, desc=desc, CONNECTIONS=3)



if __name__ == "__main__":
    server_link = "https://www.mediafire.com/file/ckkyboi75i5d5ku/%5BWitanime.com%5D+ENS+EP+01+FHD.mp4/file"
    output_dir = Path(".")
    die(download(server_link, output_dir ,"test.mp4"))