# @Author: chesterblue
# @File Name:portScan.py

from threading import Thread
import socket, queue

exist_ports = []


class Scanner(Thread):
    def __init__(self, host: str, port_queue: queue.Queue, timeout_time=2):
        super(Scanner, self).__init__()
        self.host = host
        self.timeout_time = timeout_time
        self.port_queue = port_queue

    def run(self) -> None:
        while not self.port_queue.empty():
            port = self.port_queue.get(block=True, timeout=1)
            # print("get:", port)
            scan_port = socket.socket()
            try:
                scan_port.settimeout(self.timeout_time)
                scan_port.connect((self.host, port))
                exist_ports.append(port)
                scan_port.close()
            except (TimeoutError, socket.timeout):
                scan_port.close()
            self.port_queue.task_done()


class MultiScanner:
    def __init__(self, host: str, port_list: list):
        self.host = host
        self.port_list = port_list

    def init_queue(self, port_queue, port_list):
        for port in port_list:
            port_queue.put(port)
        return port_queue

    def execute(self, thread_num=5) -> list:
        port_queue = queue.Queue(len(self.port_list))
        port_queue = self.init_queue(port_queue, self.port_list)
        for i in range(thread_num):
            t = Scanner(self.host, port_queue)
            t.start()
        port_queue.join()
        return exist_ports
