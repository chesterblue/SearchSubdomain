# @Author: chesterblue
# @File Name:GThread.py

from lib import log
from PyQt5.QtCore import QThread, pyqtSignal
import Sdl.sdlcore as sdl

class GThreadBrute(QThread):
    """自定义Thread类，实现实时输出功能"""
    # 自定义信号对象。参数str就代表这个信号可以传一个字符串
    trigger = pyqtSignal(str)
    def __init__(self, domain, dict):
        super(GThreadBrute, self).__init__()
        # 从lineEdit中获取输入的域名
        self.domain = domain
        # 从comboBox中获取的字典名
        self.dict = dict


    def run(self):
        """重写run函数,执行爆破任务"""
        log.write("[UI]get domain " + self.domain)
        # 测试环境选择直接获取字典文件
        subdomain = sdl.get_dict_contents(self.dict)
        log.write("[UI]get subdomain from dictionary " + self.dict)
        self.loop_connect_site(self.domain, subdomain)


    def loop_connect_site(self, domain, subdomain):
        """循环测试URL"""
        log.write("[UI]start http test")
        self.known_subdomain = []
        for sdom in subdomain:
            url_s = "https://%s.%s/" % (sdom, domain)
            url = "http://%s.%s/" % (sdom, domain)
            code = sdl.request_head_s(url_s)
            if sdl.isOK(code):
                self.known_subdomain.append(url_s)
                # 探测到后发送结果
                self.trigger.emit(url_s)
            else:
                code = sdl.request_head(url)
                if sdl.isOK(code):
                    self.known_subdomain.append(url)
                    # 探测到后发送结果
                    self.trigger.emit(url)
        # 探测结束后发送结束信号
        self.trigger.emit("finish")
        log.write("[UI]finish connect")
