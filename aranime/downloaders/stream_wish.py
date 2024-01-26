import re
from pathlib import Path
import requests
from aranime.utils.file_downloader import download_file
from aranime.utils import die
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
    server_link = "https://anime4low.sbs/e/czczrte7q5vc"
    output_dir = Path(".")
    file_name = "test.mp4"
    download(server_link, output_dir, file_name)