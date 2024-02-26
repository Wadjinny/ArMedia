import re
from pathlib import Path
import requests
from armedia.utils import die, debug
import m3u8_To_MP4
import logging



filter_function = lambda x: "pollllop.com" in x or "feetcdn.com" in x
priority = 10

def download(server_link, output_dir, file_name, desc=None, return_url=False):
    if return_url:
        return server_link
    headers = {
        "authority": "i.pollllop.com",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "origin": "https://rabbitstream.net",
        "Referer": "https://rabbitstream.net/",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    }
    try:
        temp_dir:Path = output_dir / "temp"
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        m3u8_To_MP4.multithread_download(server_link, file_path=output_dir / file_name,tmpdir=temp_dir,customized_http_header=headers,max_num_workers=100)
         # delete folder with all of its content
    except Exception as e:
        print(e)
        return False
    
    for file in temp_dir.glob("*"):
        file.unlink()
    temp_dir.rmdir()

    return True


if __name__ == "__main__":
    server_link = "https://q.pollllop.com/_v11/d865eff5919f3282d6684a5df3c972884ee74b731b9ae4616d5aa166a112a9d22dcc62a28ff8034421db4b64659587e25ba2296205c54f3be787ce305abcae9348d480883ede5ed8df92a8f10bfaa21eac056673b50021a96e3d2afea6ea7076f505ad28e34b5342a4c67a80c8a1004b2226a806186f9913cc46b6d13e9461981b4477e8d3ed18a081114a8b628a1b1c/playlist.m3u8"
    
    output_dir = Path(".")
    file_name = "test.mp4"
    die(download(server_link, output_dir, file_name))
