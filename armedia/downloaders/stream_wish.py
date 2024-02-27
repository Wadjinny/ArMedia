import re
from pathlib import Path
import requests
from armedia.utils.file_downloader import download_file
from armedia.utils import die

try:
    import m3u8_To_MP4
except ImportError:
    import subprocess
    import sys
    subprocess.run([sys.executable, "-m", "pip", "install", Path.home() / ".armedia/m3u8_To_MP4-0.1.12-py3-none-any.whl"], check=True)
    import m3u8_To_MP4
filter_function = lambda x: "anime4low.sb" in x
priority = 0



def download(server_link, output_dir, file_name, desc=None,return_url=False):
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
    output_dir = "./"
    # sources = "https://b-g-eu-16.feetcdn.com:2223/v3-hls-playback/aa043bbe3fc72d9663191eec94ec2d7c0f70d80dad07127c06fca45378ddb099b79d15984fe5097927a0c6e28710ce467b93f6cf892fc6a3107f82d0995a8efb378e71dfcbd7a614fbb77a5fdb2fc04e406137a5961c9186c420426d57ce751f5831c08b2afee95542f603b6d49e5f90f70a5ef9f858e89d633e9191237262473a9d56fd99a5b4f3bf75afd97240fc766c50e5eaa1cf4b63c7932c5914960878784064d08ec6714d1b6c991ab346e35c/playlist.m3u8"
    # headers =  {
    # "accept": "*/*",
    # "accept-language": "en-US,en;q=0.9",
    # "cache-control": "no-cache",
    # "pragma": "no-cache",
    # "sec-ch-ua": "\"Not A(Brand\";v=\"99\", \"Google Chrome\";v=\"121\", \"Chromium\";v=\"121\"",
    # "sec-ch-ua-mobile": "?0",
    # "sec-ch-ua-platform": "\"Linux\"",
    # "sec-fetch-dest": "empty",
    # "sec-fetch-mode": "cors",
    # "sec-fetch-site": "cross-site",
    # "Referer": "https://moviesjoy.plus/",
    # "Referrer-Policy": "strict-origin-when-cross-origin"
    # }
    
    source = "https://stream.mux.com/gqgKHavOJUOkz4hEAII4NtMEhEckE3Lp6FPLPD026clk.m3u8?token=eyJhbGciOiJSUzI1NiIsImtpZCI6Ik5CY3o3Sk5RcUNmdDdWcmo5MWhra2lEY3Vyc2xtRGNmSU1oSFUzallZMDI0IiwidHlwIjoiSldUIn0.eyJzdWIiOiJncWdLSGF2T0pVT2t6NGhFQUlJNE50TUVoRWNrRTNMcDZGUExQRDAyNmNsayIsImV4cCI6MTcwODI4MjgwMCwiYXVkIjoidiIsInBsYXliYWNrX3Jlc3RyaWN0aW9uX2lkIjoiSXIwMkZtcXNxVW5NSXBFcUg4OU1kbHZXYTE1UXdPbzZkQ25lbEN0U0k5WUkifQ.ZpBCOxJPHJ9ri6nndkDiWl22ciLcOFJEnBIJQwhZA_UARKejWAMVGVTLm8QwV7zDjWERDHrXn6XbZvxGbQw_nByT8q03fuPWqOAtTpFjr5LxoY_-C4BiZnArab--JucDGOOgGPdvjG3zfzqwEihsqwNhexRgNnp-cVlZCS-0rk0L8zY3ItktK-JrTTnxOJ0slNwXxnRlr4SzeYDEwWywEPCQxuEZZjm8KqpfwkiJfjSn3MYgLHSk7W2wW_L4lcihoFIx8e8_ed_Ge3WLwmLFOn1qFpak5nD8AZS3mwiKg15yf_aUH4GFpr4_iloKOtPkFwq4_PJn1044asAcxU_xXA"
    headers = {
    "accept": "*/*",
    "accept-language": "fr,en-US;q=0.9,en;q=0.8",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "sec-ch-ua": "\"Not A(Brand\";v=\"99\", \"Google Chrome\";v=\"121\", \"Chromium\";v=\"121\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Linux\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "Referer": "https://www.patreon.com/",
    "Referrer-Policy": "strict-origin-when-cross-origin"
  }
    m3u8_To_MP4.multithread_download(source, mp4_file_dir=output_dir, mp4_file_name="file_name.mp4", customized_http_header=headers)