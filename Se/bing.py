# @Author: chesterblue
# @File Name:bing.py.py

import re

from bs4 import BeautifulSoup
from requests import Session
from requests.exceptions import Timeout, ConnectionError

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.7113.93 '
                  'Safari/537.36',
}


class Client():
    def __init__(self, domain):
        self.headers = headers
        self.domain = domain
        self.item_num = 1
        self.base_url = "https://www.bing.com/search?q=site%%3a%s&first=%d&FORM=PERE"
        self.subdomains = []

    def run(self, total_page=3):
        # 使用session只需建立一次TCP连接
        s = Session()
        # for 循环实现获取前10页结果,经测试一页有10条结果
        for num in range(total_page):
            self.item_num = num * 10 + 1
            target = self.base_url % (self.domain, self.item_num)
            try:
                html = s.get(url=target, headers=self.headers).content.decode()
                html = BeautifulSoup(html, features="html.parser")
                self.find_subdomain(html)
            except Timeout:
                print("Timeout!")
            except ConnectionError:
                print("Internet Error!")
            except TypeError:
                print("Type Error!")
            except Exception:
                print("Unknown Error!")
        return self.subdomains

    def find_subdomain(self, html):
        re_domain = re.compile("[0-9A-Za-z]+\." + self.domain)
        for link in html.find_all('cite'):
            # 正则的作用主要是提取 https://talent.baidu.com/external/baidu/index.html 这种类型中的子域名
            if re_domain.search(link.contents[0].strip()) is not None:
                self.subdomains.append(re_domain.findall(link.contents[0].strip())[0])