# @Author: chesterblue
# @File Name:sdlGUI.py

import sys, log
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
from gui import *
import sdomlookup as sdl



class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        # listview数据存储
        self.itemmodel = QtCore.QStringListModel(self)
        self.listView.setModel(self.itemmodel)

        # start按钮绑定多线程槽函数，执行任务
        self.pushButton.clicked.connect(self.execute)

    def execute(self):
        # 获取用户输入的domain值
        self.getDomain()
        # 实例化线程对象
        self.work = MyThread(self.domain)
        # 启动线程
        self.work.start()
        # 线程自定义信号连接的槽函数
        self.work.trigger.connect(self.addUrl)

    def getDomain(self):
        """获取提交的domain值，并判断是否合法"""
        self.domain = self.lineEdit.text()


    def addRes(self,url):
        try:
            for url in self.known_subdomain:
                row = self.itemmodel.rowCount()
                self.itemmodel.insertRow(row)
                self.itemmodel.setData(self.itemmodel.index(row),url)
        except:
            pass

    def addUrl(self,url):
        """添加爆破的结果并输出"""
        if url != "finish":
            row = self.itemmodel.rowCount()
            self.itemmodel.insertRow(row)
            self.itemmodel.setData(self.itemmodel.index(row), url)
        else:
            self.alertTip()


    def alertTip(self):
        """完成任务后的提示框"""
        tip = QMessageBox.information(self,"Tip","已完成",QMessageBox.Yes | QMessageBox.No)


class MyThread(QThread):
    """自定义Thread类，实现实时输出功能"""
    # 自定义信号对象。参数str就代表这个信号可以传一个字符串
    trigger = pyqtSignal(str)
    def __init__(self, domain):
        super(MyThread, self).__init__()
        # 从lineEdit中获取输入的域名
        self.domain = domain


    def run(self):
        """重写run函数,执行爆破任务"""
        log.write("[UI]get domain " + self.domain)
        # 测试环境选择直接获取字典文件
        subdomain = sdl.get_dict_contents("./dict/test.txt")
        log.write("[UI]get subdomain from dictionary")
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())