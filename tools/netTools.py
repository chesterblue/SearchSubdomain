# @Author: chesterblue
# @File Name:netTools.py

from requests import head
from requests.exceptions import Timeout, ConnectionError


def test_proxy(proxies, url="https://www.google.com"):
    try:
        html = head(url, proxies=proxies)
        return "Proxy is OK!"
    except (Timeout, ConnectionError):
        return "Proxy error or Internet error!"
