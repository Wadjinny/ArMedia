from setuptools import setup, find_packages
from pathlib import Path
with open("requirements.txt") as f:
    requirements = f.readlines()
with open("priority.txt") as f:
    priority = f.readlines()

app_path = Path.home() / ".armedia"
app_path.mkdir(exist_ok=True)
with open(app_path / "priority.txt", "w") as f:
    f.writelines(priority)

long_description = "Download Anime/ Movies/ Series with arabic sub from public websites"

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
