# setup.py
from setuptools import setup, find_packages

setup(
    name="caching-proxy",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "caching-proxy = cache_proxy.cli:main",
        ],
    },
    python_requires=">=3.8",
)