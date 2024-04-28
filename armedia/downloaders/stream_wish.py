import re
from pathlib import Path
import requests
from armedia.utils.file_downloader import download_file
from armedia.utils import die
import m3u8_To_MP4

# try:
#     import m3u8_To_MP4
# except ImportError:
#     import subprocess
#     import sys
#     subprocess.run([sys.executable, "-m", "pip", "install", Path.home() / ".armedia/m3u8_To_MP4-0.1.12-py3-none-any.whl"], check=True)
#     import m3u8_To_MP4
filter_function = lambda x: "anime4low.sb" in x
priority = 0


def download(server_link, output_dir, file_name, desc=None, return_url=False):
    response = requests.get(server_link)
    response = response.text
    sources = re.findall(r'sources: \[\{file:"(.*?)"\}\]', response)
    if sources:
        sources = sources[0]
    else:
        return False
    if return_url:
        return sources
    m3u8_To_MP4.multithread_download(
        sources, mp4_file_dir=output_dir, mp4_file_name=file_name
    )
    return True


if __name__ == "__main__":
    output_dir = "./"
    source = "https://stream.mux.com/gqgKHavOJUOkz4hEAII4NtMEhEckE3Lp6FPLPD026clk.m3u8?token=eyJhbGciOiJSUzI1NiIsImtpZCI6Ik5CY3o3Sk5RcUNmdDdWcmo5MWhra2lEY3Vyc2xtRGNmSU1oSFUzallZMDI0IiwidHlwIjoiSldUIn0.eyJzdWIiOiJncWdLSGF2T0pVT2t6NGhFQUlJNE50TUVoRWNrRTNMcDZGUExQRDAyNmNsayIsImV4cCI6MTcwODI4MjgwMCwiYXVkIjoidiIsInBsYXliYWNrX3Jlc3RyaWN0aW9uX2lkIjoiSXIwMkZtcXNxVW5NSXBFcUg4OU1kbHZXYTE1UXdPbzZkQ25lbEN0U0k5WUkifQ.ZpBCOxJPHJ9ri6nndkDiWl22ciLcOFJEnBIJQwhZA_UARKejWAMVGVTLm8QwV7zDjWERDHrXn6XbZvxGbQw_nByT8q03fuPWqOAtTpFjr5LxoY_-C4BiZnArab--JucDGOOgGPdvjG3zfzqwEihsqwNhexRgNnp-cVlZCS-0rk0L8zY3ItktK-JrTTnxOJ0slNwXxnRlr4SzeYDEwWywEPCQxuEZZjm8KqpfwkiJfjSn3MYgLHSk7W2wW_L4lcihoFIx8e8_ed_Ge3WLwmLFOn1qFpak5nD8AZS3mwiKg15yf_aUH4GFpr4_iloKOtPkFwq4_PJn1044asAcxU_xXA"
    headers = {
        "accept": "*/*",
        "accept-language": "fr,en-US;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "Referer": "https://www.patreon.com/",
        "Referrer-Policy": "strict-origin-when-cross-origin",
    }
    m3u8_To_MP4.multithread_download(
        source,
        mp4_file_dir=output_dir,
        mp4_file_name="file_name.mp4",
        customized_http_header=headers,
    )
