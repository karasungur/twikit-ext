
from setuptools import setup, find_packages

setup(
    name="twikit-ext",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "httpx>=0.27.2",
        "loguru>=0.7.3",
        "proxystr>=2.1.3",
        "pydantic>=2.11.7",
        "pyotp>=2.9.0",
        "python-socks>=2.7.1",
        "twikit",
    ],
    python_requires=">=3.12",
)
