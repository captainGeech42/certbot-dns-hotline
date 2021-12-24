import pathlib

from setuptools import setup
from setuptools import find_packages

base_dir = pathlib.Path(__file__).resolve().parent

with open(base_dir / "requirements.txt", "r") as f:
    deps = [x.strip() for x in f.readlines()]

with open(base_dir / "README.md", "r") as f:
    readme = f.read()

setup(
    name="certbot-dns-hotline",
    version="0.3.0",
    description="Certbot DNS plugin for Hotline",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/captainGeech42/certbot-dns-hotline",
    author="Zander Work",
    author_email="pypi@zanderwork.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(),
    python_requires=">=3.6",
    include_package_data=True,
    install_requires=deps,
    entry_points={
        "certbot.plugins": [
            "dns-hotline= certbot_dns_hotline.dns_hotline:Authenticator"
        ]
    }
)