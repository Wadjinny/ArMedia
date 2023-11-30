import requests
import re
from aranime.utils.file_downloader import download_file
from aranime.utils import debug, die
from pathlib import Path

filter_function = lambda x: "dropbox.com" in x and ".mp4" in x
priority = 10

def download(server_link, output_dir, file_name, desc=None,return_url=False):
    if return_url:
        return server_link
    return download_file(server_link, output_dir, file_name, desc=desc)


# upload_links = list(filter(lambda x: "uploadourvideo.com" in x, server_links))
