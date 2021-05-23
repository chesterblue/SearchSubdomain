# @Author: chesterblue
# @File Name:sdlGUI.py

import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from Gui.gui import *
from Gui.GThread import *
import configparser
import tools.deduplicate as deduplicate
from tools import log

"""
global variable
"""
config = configparser.ConfigParser()
config.read("./conf/default.ini")
proxies = config['proxies']
virus_api_key = config['ApiKey']['virusApiKey']


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        # listview数据存储
        self.itemmodel = QtCore.QStringListModel(self)
        self.listView.setModel(self.itemmodel)
        # 可选功能的listview数据存储
        self.itemmodel_1 = QtCore.QStringListModel(self)
        self.listView_1.setModel(self.itemmodel_1)

        # 读取字典目录下所有字典名
        self.get_all_file_name()

        # start按钮绑定多线程槽函数，执行任务
        self.pushButton.clicked.connect(self.execute)

    def execute(self):
        # 获取用户输入的domain值
        self.getDomain()
        # 获取用户在comboBox选择的字典名
        self.getDictname()
        # 获取用户在spinBox中设置的线程数
        self.getThreadnum()
        # 实例化爆破子域名线程对象
        self.work = GThreadBrute(self.domain,self.dict)
        # 实例化多线程爆破子域名线程对象
        self.work = GMultiThreadBrute(self.domain, self.dict, self.thread_num)
        self.pBarWork = GProgressbar()
        # 启动线程
        self.work.start()
        self.pBarWork.start()
        self.start_optional_features(proxies, virus_api_key)
        # 线程自定义信号连接的槽函数
        self.work.trigger.connect(self.addUrl)
        # work.signal --> pBarWork.signal --> update_progressBar
        self.pBarWork.progressBarValue.connect(self.work.progressBarValue)
        self.work.progressBarValue.connect(self.update_progressBar)
    def getDomain(self):
        """获取提交的domain值，并判断是否合法"""
        self.domain = self.lineEdit.text()

    def get_all_file_name(self):
        """获取目录下所有字典文件"""
        files = os.listdir("./dict")
        for file_name in files:
            self.comboBox.addItem(file_name)

    def getDictname(self):
        """获取选择的字典文件"""
        self.dict = "./dict/" + self.comboBox.currentText()

    def getThreadnum(self):
        """获取用户输入的线程数"""
        self.thread_num = int(self.spinBox.text())

    def addRes(self, url):
        try:
            for url in self.known_subdomain:
                row = self.itemmodel.rowCount()
                self.itemmodel.insertRow(row)
                self.itemmodel.setData(self.itemmodel.index(row), url)
        except:
            pass

    def addUrl(self, url):
        """添加爆破的结果并输出"""
        if url != "finish":
            row = self.itemmodel.rowCount()
            self.itemmodel.insertRow(row)
            self.itemmodel.setData(self.itemmodel.index(row), url)
        else:
            self.alertTip()

    def alertTip(self):
        """完成任务后的提示框"""
        tip = QMessageBox.information(self, "Tip", "已完成", QMessageBox.Yes | QMessageBox.No)

    def update_progressBar(self, i):
        """更新进度条的值"""
        self.progressBar.setValue(i)

    def start_optional_features(self, proxies, virus_api_key):
        """判断并执行可选的爬虫和DNS解析功能"""
        search_engine = []
        if self.checkBox_1.isChecked():
            log.write("baidu start")
            search_engine.append("baidu")
        if self.checkBox_2.isChecked():
            log.write("bing start")
            search_engine.append("bing")
        if self.checkBox_3.isChecked():
            log.write("google start")
            search_engine.append("google")
        if search_engine:
            self.se_work = GSpider(self.domain, search_engine, proxies)
            self.se_work.start()
            self.se_work.trigger_subdomains.connect(self.get_spider_result)
        if self.checkBox_4.isChecked():
            log.write("DNS start")
            self.dns_work = GDns(self.domain, virus_api_key, proxies)
            self.dns_work.start()
            self.dns_work.trigger_subdomains.connect(self.get_dns_result)

    def get_spider_result(self, subdomains: list):
        self.itemmodel_1.setStringList(subdomains)

    def get_dns_result(self, subdomains: list):
        self.itemmodel_1.setStringList(subdomains)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())
