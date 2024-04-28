from armedia.downloaders.doodstream import download as doodstream_download
from armedia.downloaders.downet import download as downet_download
from armedia.downloaders.drive import download as drive_download
from armedia.downloaders.dropbox import download as dropbox_download
from armedia.downloaders.ds2play import download as ds2play_download
from armedia.downloaders.mediafire import download as mediafire_download
from armedia.downloaders.meganz import download as meganz_download
from armedia.downloaders.pollllop import download as pollllop_download
from armedia.downloaders.okru import download as okru_download
from armedia.downloaders.streamtape import download as streamtape_download
from armedia.downloaders.uploadourvideo import download as uploadourvideo_download
from armedia.downloaders.stream_wish import download as stream_wish_download
from armedia.downloaders.soraplay import download as soraplay_download
from armedia.downloaders.shahidha import download as shahidha_download

import pytest

downloaders = {
    "doodstream": {
        "download": doodstream_download,
        "link": "https://d000d.com/e/q9hysf878jcl",
    },
    "downet": {
        "download": downet_download,
        "link": "https://s216d1.downet.net/download/1707152401/65bfc291ada5c/Rose.Wa.Layla.S01E08.1080p.WEB-DL.AKWAM.mp4",
    },
    "drive": {
        "download": drive_download,
        "link": "https://drive.usercontent.google.com/download?id=1B8aF0FLYOct3aOVhI_jdi8uoLz4CyFPc&export=download&authuser=0",
    },
    "dropbox": {
        "download": dropbox_download,
        "link": "https://www.dropbox.com/s/5z8b1k6z4c4f2y8/1.mp4?dl=0",
    },
    "ds2play": {
        "download": ds2play_download,
        "link": "https://ds2play.com/e/8ge1hg1bjt1r",
    },
    "mediafire": {
        "download": mediafire_download,
        "link": "https://www.mediafire.com/file/ckkyboi75i5d5ku/%5BWitanime.com%5D+ENS+EP+01+FHD.mp4/file",
    },
    "meganz": {
        "download": meganz_download,
        "link": "https://mega.nz/file/dnczXRxD#s9TXCr2rVDwNx9OCO1FH-lNRK2OVyWahgR6LwwsPNYU",
    },
    "pollllop": {
        "download": pollllop_download,
        "link": "https://q.pollllop.com/_v11/d865eff5919f3282d6684a5df3c972884ee74b731b9ae4616d5aa166a112a9d22dcc62a28ff8034421db4b64659587e25ba2296205c54f3be787ce305abcae9348d480883ede5ed8df92a8f10bfaa21eac056673b50021a96e3d2afea6ea7076f505ad28e34b5342a4c67a80c8a1004b2226a806186f9913cc46b6d13e9461981b4477e8d3ed18a081114a8b628a1b1c/playlist.m3u8",
    },
    "okru": {"download": okru_download, "link": "https://ok.ru/video/7318166506059"},
    "streamtape": {
        "download": streamtape_download,
        "link": "https://streamtape.cc/e/Gvl4Z3JlyXFAmY",
    },
    # need a link
    # "uploadourvideo": {
    #     "download": uploadourvideo_download,
    #     "link": "https://uploadourvideo.com/e/5s5",
    # },
    # need a link
    # "stream_wish": {
    #     "download": stream_wish_download,
    #     "link": "https://stream.mux.com/gqgKHavOJUOkz4hEAII4NtMEhEckE3Lp6FPLPD026clk.m3u8?token=eyJhbGciOiJSUzI1NiIsImtpZCI6Ik5CY3o3Sk5RcUNmdDdWcmo5MWhra2lEY3Vyc2xtRGNmSU1oSFUzallZMDI0IiwidHlwIjoiSldUIn0.eyJzdWIiOiJncWdLSGF2T0pVT2t6NGhFQUlJNE50TUVoRWNrRTNMcDZGUExQRDAyNmNsayIsImV4cCI6MTcwODI4MjgwMCwiYXVkIjoidiIsInBsYXliYWNrX3Jlc3RyaWN0aW9uX2lkIjoiSXIwMkZtcXNxVW5NSXBFcUg4OU1kbHZXYTE1UXdPbzZkQ25lbEN0U0k5WUkifQ.ZpBCOxJPHJ9ri6nndkDiWl22ciLcOFJEnBIJQwhZA_UARKejWAMVGVTLm8QwV7zDjWERDHrXn6XbZvxGbQw_nByT8q03fuPWqOAtTpFjr5LxoY_-C4BiZnArab--JucDGOOgGPdvjG3zfzqwEihsqwNhexRgNnp-cVlZCS-0rk0L8zY3ItktK-JrTTnxOJ0slNwXxnRlr4SzeYDEwWywEPCQxuEZZjm8KqpfwkiJfjSn3MYgLHSk7W2wW_L4lcihoFIx8e8_ed_Ge3WLwmLFOn1qFpak5nD8AZS3mwiKg15yf_aUH4GFpr4_iloKOtPkFwq4_PJn1044asAcxU_xXA",
    # },
    # # need a link
    # "soraplay": {
    #     "download": soraplay_download,
    #     "link": "https://soraplay.xyz/embed/5QDgM8nSke17f/",
    # },
}


@pytest.mark.parametrize(
    "downloader",
    downloaders.values(),
    ids=downloaders.keys(),
)
def test_download(downloader):

    link = downloader["link"]
    downloader_func = downloader["download"]
    result = downloader_func(link, ".", "test.mp4", return_url=True)
    assert result
