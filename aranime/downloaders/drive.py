import re
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from aranime.utils.file_downloader import download_file
from aranime.utils import die


filter_function = lambda x: "drive.google.com" in x
priority = 13

headers = {
    "AUTH_26fp55mq9v5i1ab34k205tqijo4ca64c": "03862451855875902521Z|1700877675000|ps1rgn3alt74f8mufgket0rvp6dhfa98",
    "COMPASS": "documents=CmIACWuJV2-ZChMhtx2-iD7f3KgeGOh7QSKVgjBtbUVCXSm7Z-K0SGmbmxGjGDGx-tzVeNFxR2l6_85-a2KZjjJXwOpELK-q1FVqCVkXClK8iAeuHUvFBxLgXLnZQO9xnDvOdBDx_vSmBhpkAAlriVc9_tbGja0SOveLBupSqpAC_3MXi_oKvLaH6vMxSrr8qqNkMv97MOsLLhmq3Sc-nPcQtP0GdpJngU4Dn5Gqpr2qw7i3A9q1zplyNuBG6fDjwXoJWXqCVMRR_nw93-hVpQ==",
    "GFE_RTT": "257",
    "NID": "511=BRHhRFz3aTBU_d9GiZWI0gFtidXfP27uGkufeGyUvdNiPWbJvWb8ccJME-9Qp9Ec9too8hl-cqwsNbIV--d3MlvzshkBt0qFII_SdOmvhVWdY-lutV15k5z6ATR6bRyLyp16eriKWIGNurKo3q2v8wl6niGjflVVK0CdJQQ2Fxs",
}


def download(server_link, output_dir, file_name, desc=None, return_url=False):
    def get_id(link):
        if "export=download" in link:
            return re.findall(r"id=(.*)", link)[0]
        else:
            return re.findall(r"/d/(.*?)/", link)[0]

    id = get_id(server_link)
    url = f"https://drive.google.com/uc?id={id}&export=download"
    session = requests.Session()
    session.headers.update(headers)
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
    return download_file(download_url, output_dir, file_name, desc=desc, CONNECTIONS=1,session=session)


if __name__ == "__main__":
    server_link = (
        "https://drive.google.com/file/d/1EzbVC-6O5XhTELRYsVrC4X5D-ivJxKDC/preview"
    )
    output_dir = Path(".")
    file_name = "test.mp4"
    die(download_file(server_link, output_dir, file_name))
