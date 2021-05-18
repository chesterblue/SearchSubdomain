# @Author: chesterblue
# @File Name:baidu.py.py

from requests import Session
from requests.exceptions import Timeout, ConnectionError
from bs4 import BeautifulSoup
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.7113.93 '
                  'Safari/537.36',
    # 'Cookie' : r'PSTM=1586448233; BIDUPSID=1AD00D110A0EAE0E6779BC5B1421E54F; BD_UPN=12314753; '
    #             'BAIDUID=85AB0ED2CCC076605AD80499F6F08F52:FG=1; '
    #             'BDSFRCVID_BFESS=Qf4OJexroG38FIRe7cR7oAGG4eKKvV3TDYLEIXH30kmA-6kVgaSTEG0Pt8lgCZu-2ZlgogKKBmOTHgLF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; '
    #             'H_BDCLCKID_SF_BFESS=tRk8oI0aJDvjDb7GbKTMbtCSbfTJetJyaR3v5DbvWJ5WqR7jDT7mQMI8jUrEXPRC3KtJ0lvcbfL5ShbXXM'
    #             'o10nIVeH8DKb5NWGcwhD5S3l02V-bv-fJf5qRDhpAO04RMW23GWl7mWn3dsxA45J7cM4IseboJLfT-0bc4KKJxbnLWeIJEjjCajT'
    #             'cQjN_qq-jeHDrKBRbaHJOoDDvK2MOcy4LbKxnxJ5vT3n7-_bTLyn7Nsn4mbfRv5l5y3-OkWn39babTQ-tbBp3k8MQ8W6osQfbQ0hOy'
    #             '5xbbbG8LW-Py3R7JOpvthfnxy--TQRPH-Rv92DQMVU52QqcqEIQHQT3m5-5bbN3ut6IqJb-qoDKbfbOSjJOcq4QSMJF0hmT22-usL'
    #             'CFJ2hcHMPoosI89QxrCbj-S0GJy3xbxJITia-QCtMbUoqRHyq71DT8fhtLLttnp5K6g-p5TtUJMbbRTLp6hqjDlhMJyKMni0Dj9-p'
    #             'njBpQrh459XP68bTkA5bjZKxtq3mkjbPbDfn028DKu-n5jHj30ja8D3e; __yjs_duid=1_79ecbe729ab48b3dfa43a5f81bb4d0'
    #             'ac1620145669146; H_WISE_SIDS=107317_110085_127969_131423_154619_165136_166147_167729_169066_169445_17'
    #             '0142_170816_170873_170936_171234_171565_172226_172535_172643_172828_172866_172923_173125_173414_17360'
    #             '2_173610_173625_173635_173949_174179_174199_174358_174438_174447_174592_174662_174670_174682_174831_17'
    #             '4855_175097_175216_175365; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=33839_33814_34004_33607'
    #             '_34026; sug=3; sugstore=1; ORIGIN=0; bdime=0; delPer=0; BD_CK_SAM=1; PSINO=1; H_PS_645EC=ed5eLvpUNR8j7'
    #             'S8%2FDTAxa76nt0h0xDGnXZ89j9lVYcUl3LCMNzb8v%2FGugNM; BA_HECTOR=aka52505ah812h8g9d1g9sm8m0q; BDSVRTM=15'
    #             '0; WWW_ST=1620990238326'
}


class Client():
    def __init__(self, domain):
        self.domain = domain
        self.headers = headers
        self.page_num = 0
        self.base_url = "https://www.baidu.com/s?wd=site%%3a%s&pn=%d"
        self.subdomains = []

    def run(self, total_page=3):
        # 使用session只需建立一次TCP连接
        s = Session()
        for num in range(total_page):
            self.page_num = num * 10
            target = self.base_url % (self.domain, self.page_num)
            try:
                html = s.get(target, headers=self.headers).content.decode()
                # print(html)
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
        for item in html.find_all('a'):
            if self.is_value(item):
                if self.get_subdomain(item):
                    self.subdomains.append(self.get_subdomain(item))

    def is_value(self, item):
        """
        判断是否是展示子域名的<a target="_blank" class="c-showurl c-color-gray" style="text-decoration:none;
        position:relative;">Bing</a>
        经过分析当class值为c-showurl c-color-gray时是显示域名的链接
        """
        try:
            if item['class'][0] == 'c-showurl':
                return True
            else:
                return False
        except:
            return False

    def get_subdomain(self, item):
        """
        使用正则匹配子域名，如若不存在返回False；
        因为有些标签值为文字或者链接，通过此函数直接筛选过滤为目标值并返回结果
        """
        re_domain = re.compile("[0-9A-Za-z]+\." + self.domain)
        if re_domain.search(item.contents[0].strip()) is not None:
            return re_domain.findall(item.contents[0].strip())[0]
        else:
            return False
