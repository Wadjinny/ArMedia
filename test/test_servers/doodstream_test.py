from armedia.downloaders.doodstream import download


def test_download():
    link = "https://d0o0d.com/e/mtxij6jgkp9s"
    result = download(link, None, None, return_url=True)
    print(result)
    assert bool(result)
    
if __name__ == "__main__":
    test_download()