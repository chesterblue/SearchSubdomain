# @Author: chesterblue
# @File Name:google.py.py

import re

from bs4 import BeautifulSoup
from requests import Session
from requests.exceptions import Timeout, ConnectionError
from tools import log

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.7113.93 '
                  'Safari/537.36',
}


class Client():
    def __init__(self, domain, proxies=None):
        self.domain = domain
        self.headers = headers
        self.proxies = proxies
        self.page_num = 0
        self.base_url = "https://www.google.com/search?q=site%%3a%s&start=%d"
        self.subdomains = []

    def run(self, total_page=3):
        # 使用session只需建立一次TCP连接
        s = Session()
        for num in range(total_page):
            page_num = num * 10
            target = self.base_url % (self.domain, page_num)
            try:
                html = s.get(target, headers=self.headers, proxies=self.proxies, verify=False).content.decode()
                html = BeautifulSoup(html, features="html.parser")
                self.find_subdomain(html)
            except Timeout:
                log.write("spider:google:Timeout!")
            except ConnectionError:
                log.write("spider:google:Internet Error!")
            except TypeError:
                log.write("spider:google:Type Error!")
            except Exception as e:
                log.write("spider:google:Unknown Error!")
                print(e)
        return self.subdomains

    def find_subdomain(self, html):
        re_domain = re.compile("[0-9A-Za-z]+\." + self.domain)
        for link in html.find_all('cite'):
            # 正则的作用主要是提取 https://talent.baidu.com/external/baidu/index.html 这种类型中的子域名
            if re_domain.search(link.contents[0].strip()) is not None:
                self.subdomains.append(re_domain.findall(link.contents[0].strip())[0])

