import requests
import re
from armedia.utils.file_downloader import download_file



filter_function = lambda x: ("soraplay.xyz/embed" in x) and ("mirror" not in x)
priority = 9
def download(server_link, output_dir, file_name, desc=None,return_url=False):
    session = requests.Session()
    session.headers.update({"Referer": "https://witanime.pics/"})
    response = session.get(server_link)
    response = response.text

    link = re.findall(r'"file":"(.*?)"', response)
    if link:
        link = link[0]
    else:
        return False
    
    if return_url:
        return link
    return download_file(link, output_dir, file_name, desc=desc)


if __name__ ==  "__main__":
    link = "https://soraplay.xyz/embed/5QDgM8nSke17f/"