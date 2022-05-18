import setuptools
from config import Config

with open("README.md", "r", encoding='UTF8') as fh:
    long_description = fh.read()

setuptools.setup(
    name=Config.APP_NAME,
    version=Config.API_VERSION,
    author=Config.APP_AUTHOR,
    author_email=Config.APP_AUTHOR_EMAIL,
    description=Config.API_DESC,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://skhynix.github.com/"+Config.APP_NAME,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)