# @Author: chesterblue
# @File Name:threadcrowd.py.py


from requests import get
from requests.exceptions import Timeout, ConnectionError
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.packages.urllib3 import disable_warnings
import json

# 禁用由于不验证ssl证书导致的警告
disable_warnings(InsecureRequestWarning)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.7113.93 '
                  'Safari/537.36',
}
proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'https://127.0.0.1:7890'
}


class Client():
    def __init__(self, domain):
        self.domain = domain
        self.headers = headers
        self.base_url = "https://www.threatcrowd.org/searchApi/v2/domain/report/?domain=%s"
        self.subdomains = []

    def run(self):
        target = self.base_url % self.domain
        try:
            html = get(url=target, headers=self.headers, proxies=proxies, verify=False).content.decode()
            jdata = json.loads(html)
            self.get_subdomains(jdata)
        except (Timeout, ConnectionError):
            print("Proxy error or Internet error!")
        except Exception:
            print("Unknown error!")
        except json.decoder.JSONDecodeError:
            print("")
        finally:
            return self.subdomains

    def get_subdomains(self, jdata):
        self.subdomains = jdata['subdomains']