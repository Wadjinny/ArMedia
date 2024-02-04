import re
from pathlib import Path
import requests
from armedia.utils.file_downloader import download_file
from armedia.utils import die
import m3u8_To_MP4
import logging
logging.getLogger("m3u8downloader").setLevel(logging.WARNING)



filter_function = lambda x: "anime4low.sb" in x
priority = 0



def download(server_link, output_dir, file_name, desc=None,return_url=False):
    #sources: [{file:"https://ppgsamilsxto.sw-cdnstream.com/hls2/01/02395/czczrte7q5vc_h/master.m3u8?t=juBJm0v8FqtkiRY2wPvFfX1vNUWWD3X2Tqv9TvanrwU&s=1701301357&e=129600&f=11979029&srv=tszfjzanyeke&i=0.4&sp=500&p1=tszfjzanyeke&p2=tszfjzanyeke&asn=15557"}],
    response = requests.get(server_link)
    response = response.text
    sources = re.findall(r'sources: \[\{file:"(.*?)"\}\]', response)
    if sources:
        sources = sources[0]
    else:
        return False
    if return_url:
        return sources
    m3u8_To_MP4.multithread_download(sources, mp4_file_dir=output_dir, mp4_file_name=file_name)
    return True
    
    

if __name__ == "__main__":
    # server_link = "https://anime4low.sbs/e/czczrte7q5vc"
    # output_dir = Path(".")
    # file_name = "test.mp4"
    # download(server_link, output_dir, file_name)
    sources = "https://b-g-eu-16.feetcdn.com:2223/v3-hls-playback/aa043bbe3fc72d9663191eec94ec2d7c0f70d80dad07127c06fca45378ddb099b79d15984fe5097927a0c6e28710ce467b93f6cf892fc6a3107f82d0995a8efb378e71dfcbd7a614fbb77a5fdb2fc04e406137a5961c9186c420426d57ce751f5831c08b2afee95542f603b6d49e5f90f70a5ef9f858e89d633e9191237262473a9d56fd99a5b4f3bf75afd97240fc766c50e5eaa1cf4b63c7932c5914960878784064d08ec6714d1b6c991ab346e35c/playlist.m3u8"
    output_dir = "./"
    headers =  {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "sec-ch-ua": "\"Not A(Brand\";v=\"99\", \"Google Chrome\";v=\"121\", \"Chromium\";v=\"121\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Linux\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "Referer": "https://moviesjoy.plus/",
    "Referrer-Policy": "strict-origin-when-cross-origin"
    }
    m3u8_To_MP4.multithread_download(sources, mp4_file_dir=output_dir, mp4_file_name="file_name.mp4", customized_http_header=headers)