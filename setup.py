from setuptools import setup, find_packages
from pathlib import Path
import subprocess
import sys
import os

with open("requirements.txt") as f:
    requirements = f.readlines()
with open("priority.txt") as f:
    priority = f.readlines()

app_path = Path.home() / ".armedia"
app_path.mkdir(exist_ok=True)

app_priority = app_path / "priority.txt"
if not app_priority.exists():
    app_priority.write_text(priority)

config_file = app_path / "config.json"
if not config_file.exists():
    config_file.write_text("{}")

long_description = "Download Anime/ Movies/ Series with arabic sub from public websites"

# m3u8_to_mp4 = "https://github.com/Wadjinny/ArMedia/raw/main/lib/m3u8_To_MP4-0.1.12-py3-none-any.whl"
# m3u8_to_mp4_path = app_path / "m3u8_To_MP4-0.1.12-py3-none-any.whl"
# subprocess.run(["wget", m3u8_to_mp4, "-O", str(m3u8_to_mp4_path)], check=True)
# m3u8_path = Path(__file__).parent / "lib/m3u8_To_MP4-0.1.12-py3-none-any.whl"
# copy m3u8_To_MP4-0.1.12-py3-none-any.whl to app_path
# m3u8_to_mp4_path = app_path / "m3u8_To_MP4-0.1.12-py3-none-any.whl"
# if not m3u8_to_mp4_path.exists():
#     m3u8_to_mp4_path.write_bytes(m3u8_path.read_bytes())

setup(
    name="armedia",
    version="1.0.0",
    author="ilyas wadjinny",
    description="Download Anime/ Movies/ Series with arabic sub ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "armedia = armedia.__main__:run",
        ]
    },
    install_requires=requirements,
    zip_safe=False,
)
