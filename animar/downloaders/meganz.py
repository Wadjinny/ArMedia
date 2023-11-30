# %% %%
import requests
import re
from pathlib import Path
import subprocess

filter_function = lambda x: "mega.nz" in x
priority = 0
def download(server_link, output_dir, file_name,return_url=False):
    # megatools is required, check if it is installed, dont display output
    if return_url:
        return server_link
    server_link = server_link.replace("embed", "file")
    try:
        subprocess.run(["megadl", "--version"], stdout=subprocess.DEVNULL, check=True)
    except FileNotFoundError:
        print("megatools is required")
        return False
    try:
        subprocess.run(
            ["megadl", server_link, "--path", str(output_dir / file_name)], check=True
        )
        return True
    except subprocess.CalledProcessError:
        print(f"Error downloading {server_link}")
