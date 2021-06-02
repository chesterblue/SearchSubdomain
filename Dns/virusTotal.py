# @Author: chesterblue
# @File Name:virusTotal.py

from requests import Session
from requests.exceptions import Timeout, ConnectionError
import json
from tools import log

headers = {
    'X-Apikey': ''
}


class Client():
    def __init__(self, domain: str, key: str):
        self.domain = domain
        self.headers = headers
        self.headers['X-Apikey'] = key
        self.base_url = "https://www.virustotal.com/api/v3/domains/%s/subdomains" % self.domain
        self.subdomains = []
        self.s = Session()

    def run(self, total_page=3):
        """
        建议total_page的值不要超过4，因为免费AIP一分钟内只能使用4次API
        """
        if self.is_key_right():
            log.write("virusTotal:API Key is right.Keep going!")
            jdata = self.connect_site_to_get_data(self.base_url)
            for page_num in range(total_page-1):
                if self.is_have_next(jdata):
                    jdata = self.connect_site_to_get_data(jdata['links']['next'])
                else:
                    break
            return self.subdomains

    def connect_site_to_get_data(self, target_url):
        try:
            html = self.s.get(url=target_url, headers=self.headers).content.decode()
            jdata = json.loads(html)
            self.get_subdomain(jdata)
            return jdata
        except (Timeout, ConnectionError):
            log.write("DNS-virusTotal:Proxy error or Internet error!")
            return None

    def is_have_next(self, jdata):
        try:
            next_url = jdata['links']['next']
            return True
        except:
            return False

    def get_subdomain(self, jdata):
        """
        从返回的json数据中获取子域名并存储数据
        """
        try:
            for link in jdata['data']:
                self.subdomains.append(link['id'])
        except KeyError:
            log.write("Maybe you have not enough API quota allowances.Or your network is not good.")


    def is_key_right(self):
        test_url = "https://www.virustotal.com/api/v3/domains/baidu.com/subdomains"
        try:
            html = self.s.get(test_url, headers=headers).text
            jdata = json.loads(html)
            try:
                # 如果有error值则表示API_KEY 有错
                if jdata['error']['code'] == 'WrongCredentialsError':
                    return False
            except:
                return True
        except (Timeout, ConnectionError):
            log.write("Proxy error or Internet error!")
            return False