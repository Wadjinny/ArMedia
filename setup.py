from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.readlines()

long_description = "Download anime with arabic sub from public websites"

setup(
    name="aranime",
    version="1.0.0",
    author="ilyas wadjinny",
    description="Download anime with arabic sub ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "aranime = aranime.__main__:run",
        ]
    },
    install_requires=requirements,
    zip_safe=False,
)
