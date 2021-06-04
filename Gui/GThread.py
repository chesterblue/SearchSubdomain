# @Author: chesterblue
# @File Name:GThread.py

from tools import log
from PyQt5.QtCore import QThread, pyqtSignal
from math import floor
import Sdl.sdlcore as sdl
from threading import Thread
from Se import baidu, bing, google
from Dns import threadcrowd, virusTotal
import queue
import tools.deduplicate as deduplicate


class GThreadBrute(QThread):
    """自定义Thread类，实现实时输出功能"""
    # 自定义信号对象。参数str就代表这个信号可以传一个字符串
    trigger = pyqtSignal(str)
    # 自定义信号，更新进度条
    progressBarValue = pyqtSignal(int)

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
        # 计算得到字典中子域名的个数，主要为进度条准备
        self.subdomainCount = len(subdomain)
        log.write("[UI]get subdomain from dictionary " + self.dict)
        self.loop_connect_site(self.domain, subdomain)

    def loop_connect_site(self, domain, subdomain):
        """循环测试URL"""
        log.write("[UI]start http test")
        self.known_subdomain = []
        # 计数，计算进度条的值
        count = 0
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
            count += 1
            # 计算并发送进度条的值给进度条线程
            self.progressBarValue.emit(self.alg(count, self.subdomainCount))
        # 探测结束后发送结束信号
        self.trigger.emit("finish")
        log.write("[UI]finish connect")

    def alg(self, dividend, divisor):
        """计算进度条，dividend:被除数 divisor：除数"""
        return floor((dividend / divisor) * 100)


class GProgressbar(QThread):
    """GUI窗口中进度条的子线程"""
    progressBarValue = pyqtSignal(int)  # 更新进度条

    def __init__(self):
        super(GProgressbar, self).__init__()

    def __del__(self):
        self.wait()


class GMultiThreadBrute(QThread):
    # 自定义信号对象。参数str就代表这个信号可以传一个字符串
    trigger = pyqtSignal(str)
    # 自定义信号，更新进度条
    progressBarValue = pyqtSignal(int)
    # 声明已发送的任务数量，初始值为0
    transmited_count = 0

    def __init__(self, domain, dict, thread_num):
        super(GMultiThreadBrute, self).__init__()
        # 从lineEdit中获取输入的域名
        self.domain = domain
        # 从comboBox中获取的字典名
        self.dict = dict
        # 从spinBox中获取的线程数
        self.thread_num = thread_num

    def run(self):
        """重写run函数,执行爆破任务"""
        log.write("[UI]get domain " + self.domain)
        # 测试环境选择直接获取字典文件
        subdomain = sdl.get_dict_contents(self.dict)
        # 计算得到字典中子域名的个数，主要为进度条准备
        self.subdomainCount = len(subdomain)
        log.write("[UI]get subdomain from dictionary " + self.dict)
        # 创建多线程传送数据所需的队列
        search_queue = queue.Queue(len(subdomain))
        log.write("[UI]finish new queue " + str(self.thread_num))
        self.init_queue(search_queue, subdomain)
        log.write("[UI]Init queue")
        self.multi_queue_connect(self.domain, search_queue, self.thread_num, self.connect_site)
        log.write("[UI]finish connect")
        search_queue.join()

    # 循环测试每个子站点
    def connect_site(self, search_queue, domain):
        self.known_subdomain = []
        while not search_queue.empty():
            sdom = search_queue.get(block=True, timeout=1)
            url_s = "https://%s.%s/" % (sdom, domain)
            url = "http://%s.%s/" % (sdom, domain)
            code = sdl.request_head_s(url_s)
            # log.write(url_s)
            if sdl.isOK(code):
                self.known_subdomain.append(url_s)
                # sdl.printRightResult(url_s)
                self.trigger.emit(url_s)
            else:
                # log.write(url)
                code = sdl.request_head(url)
                if sdl.isOK(code):
                    self.known_subdomain.append(url)
                    # sdl.printRightResult(url)
                    self.trigger.emit(url)
            search_queue.task_done()
            self.transmit_finishd_count(search_queue.unfinished_tasks)

    # 初始化队列
    def init_queue(self, search_queue, subdomain):
        for i in subdomain:
            search_queue.put(i)

    # 多线程
    def multi_queue_connect(self, domain, search_queue, thread_num, target_func):
        for i in range(thread_num):
            t = Thread(target=target_func, args=(search_queue, domain))
            t.start()
        # print(search_queue.unfinished_tasks)

    def alg(self, dividend, divisor):
        """计算进度条，dividend:被除数 divisor：除数"""
        return floor((dividend / divisor) * 100)

    def transmit_finishd_count(self, unfinisd_count):
        """通过queue中的unfinished_tasks属性计算进度条所需的值并发送给进度条"""
        all_task_count = self.subdomainCount
        finished_count = all_task_count - unfinisd_count
        if unfinisd_count == 0:
            self.progressBarValue.emit(100)
            # 探测结束后发送结束信号
            self.trigger.emit("finish")
            log.write("[UI]finish connect")
        elif self.transmited_count != finished_count:
            # 计算并发送进度条的值给进度条线程
            self.progressBarValue.emit(self.alg(finished_count, self.subdomainCount))
            # 发送后更新已发送的值
            self.transmited_count = finished_count


class GSpider(QThread):
    # 自定义信号对象。参数list就代表这个信号可以传一个列表
    #
    trigger_subdomains = pyqtSignal(list)
    # 发送结束或开始信号
    trigger_tip = pyqtSignal(str)

    def __init__(self, domain: str, search_engines: list, proxies=None):
        super(GSpider, self).__init__()
        self.domain = domain
        self.search_engines = search_engines
        self.proxies = proxies
        self.subdomains = []

    def run(self):
        self.trigger_tip.emit("start")
        for client in self.search_engines:
            if client == 'baidu':
                Baidu = baidu.Client(self.domain)
                self.subdomains.extend(Baidu.run())
            elif client == 'google':
                Google = google.Client(self.domain, proxies=self.proxies)
                self.subdomains.extend(Google.run())
            elif client == 'bing':
                Bing = bing.Client(self.domain)
                self.subdomains.extend(Bing.run())
        self.subdomains = deduplicate.remove_duplicate_data(self.subdomains)
        self.trigger_subdomains.emit(self.subdomains)
        log.write("[UI]Spider finished")
        self.trigger_tip.emit("finish")
        # return self.subdomains


class GDns(QThread):
    # 自定义信号对象。参数list就代表这个信号可以传一个列表
    #
    trigger_subdomains = pyqtSignal(list)
    # 发送结束或开始信号
    trigger_tip = pyqtSignal(str)

    def __init__(self, domain: str, virus_api_key: str, proxies=None):
        super(GDns, self).__init__()
        self.domain = domain
        self.virus_api_key = virus_api_key
        self.proxies = proxies
        self.subdomains = []

    def run(self):
        self.trigger_tip.emit("start")
        # VirusTotal DNS resolution
        VirusTotal = virusTotal.Client(self.domain, self.virus_api_key)
        results = VirusTotal.run()
        if results:
            self.subdomains.extend(results)
        # threadcrowd DNS resolution
        ThreadCrowd = threadcrowd.Client(self.domain, self.proxies)
        self.subdomains.extend(ThreadCrowd.run())
        self.subdomains = deduplicate.remove_duplicate_data(self.subdomains)
        self.trigger_subdomains.emit(self.subdomains)
        log.write("[UI]DNS finished")
        self.trigger_tip.emit("finish")
        # return self.subdomains


class GStatusbar(QThread):
    """GUI窗口中的状态栏子线程"""
    statusBarValue = pyqtSignal(str)  # 状态栏

    def __init__(self):
        super(GStatusbar, self).__init__()