# @Author: chesterblue
# @File Name:sdlGUI.py

import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from Gui.gui import *
from Gui.GThread import *
import configparser
import tools.deduplicate as deduplicate
from tools.netTools import test_proxy
from tools import log
from time import sleep

"""
global variable
"""
config = configparser.ConfigParser()
config.read("./conf/default.ini")
proxies = config['proxies']
virus_api_key = config['ApiKey']['virusapikey']

class SetAPI(QMainWindow, Ui_SetAPI):
    def __init__(self):
        super(SetAPI, self).__init__()
        self.setupUi(self)
        self.show_api_key()
        self.buttonBox.rejected.connect(self.close)
        self.buttonBox.accepted.connect(self.save_api_key)

    def show_api_key(self):
        """
        获取api值并显示在UI界面
        """
        self.virus_api_key_value.setText(virus_api_key)

    def save_api_key(self):
        virus_api_key = self.virus_api_key_value.text()
        config.set('ApiKey', 'virusapikey', virus_api_key)
        with open('./conf/default.ini','w+') as fp:
            config.write(fp)
        self.close()


class TestProxy(QMainWindow, Ui_TestProxy):
    def __init__(self):
        super(TestProxy, self).__init__()
        self.setupUi(self)
        self.buttonBox.rejected.connect(self.close)
        self.buttonBox.accepted.connect(self.connect_test)

    def connect_test(self):
        url = self.lineEdit.text()
        res = test_proxy(proxies, url)
        QMessageBox.information(self, "Tip", res, QMessageBox.Yes | QMessageBox.No)


class SetProxy(QMainWindow, Ui_SetProxy):
    def __init__(self):
        super(SetProxy, self).__init__()
        self.setupUi(self)
        self.show_proxies()

        # 实例化TestProxy对象
        self.test_proxy_window = TestProxy()

        self.testProxyButton.clicked.connect(self.test_proxy_window.show)
        self.buttonBox.rejected.connect(self.close)

        # 确定按钮绑定存储代理的函数
        self.buttonBox.accepted.connect(self.save_configure)

    def show_proxies(self):
        self.http_address.setText(proxies['http'].split(':')[1].strip('//'))
        self.http_port.setValue(int(proxies['http'].split(':')[2]))
        self.https_address.setText(proxies['https'].split(':')[1].strip('//'))
        self.https_port.setValue(int(proxies['https'].split(':')[2]))

    def save_configure(self):
        proxies['http'] = 'http://'+self.http_address.text()+':'+self.http_port.text()
        proxies['https'] = 'https://'+self.https_address.text()+':'+self.https_port.text()
        config.set('proxies', 'http', proxies['http'])
        config.set('proxies', 'https', proxies['https'])
        with open('./conf/default.ini','w+') as fp:
            config.write(fp)
        self.close()


class MyWindow(QMainWindow, Ui_MainWindow):
    brute_subdomains = []
    dns_subdomains = []
    spider_subdomains = []
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

        # 实例化proxy对象和api_key对象
        self.set_proxy_window = SetProxy()
        self.set_api_window = SetAPI()
        # 实例化文件对象
        self.export_result_window = QtWidgets.QFileDialog(self,'导出结果')
        # 实例化状态栏线程对象
        self.sBarWork = GStatusbar()
        self.sBarWork.start()

        # 设置菜单
        self.actionproxy.triggered.connect(self.set_proxy_window.show)
        self.actionAPI_Key.triggered.connect(self.set_api_window.show)
        # 工具菜单
        self.actionexport.triggered.connect(self.export_results_to_file)

        # start按钮绑定多线程槽函数，执行任务
        self.pushButton.clicked.connect(self.execute)

    def execute(self):
        # 获取用户输入的domain值
        self.getDomain()
        if self.brute_checkBox.isChecked():
            self.start_brute()
        self.start_optional_features(proxies, virus_api_key)


    def start_brute(self):
        # 获取用户在comboBox选择的字典名
        self.getDictname()
        # 获取用户在spinBox中设置的线程数
        self.getThreadnum()
        # 实例化爆破子域名线程对象
        self.work = GThreadBrute(self.domain, self.dict)
        # 实例化多线程爆破子域名线程对象
        self.work = GMultiThreadBrute(self.domain, self.dict, self.thread_num)
        self.pBarWork = GProgressbar()

        # 启动线程
        self.work.start()
        self.pBarWork.start()
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

    def addUrl(self, url):
        """添加爆破的结果并输出"""
        if url != "finish":
            # 存储爆破模块结果以便导出
            self.brute_subdomains.append(url)
            row = self.itemmodel.rowCount()
            self.itemmodel.insertRow(row)
            self.itemmodel.setData(self.itemmodel.index(row), url)
        else:
            self.alertTip()

    def alertTip(self):
        """完成任务后的提示框"""
        tip = QMessageBox.information(self, "Tip", "爆破已完成", QMessageBox.Yes | QMessageBox.No)

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
            # 状态栏提示信息，信号传递方向：se_work.signal --> sBarWork.signal --> show_status_bar
            self.sBarWork.statusBarValue.connect(self.se_work.trigger_tip)
            self.se_work.trigger_tip.connect(self.show_status_bar)
            self.se_work.start()
            self.se_work.trigger_subdomains.connect(self.show_spider_result)
        if self.checkBox_4.isChecked():
            log.write("DNS start")
            self.dns_work = GDns(self.domain, virus_api_key, proxies)
            # 状态栏提示信息，信号传递方向：se_work.signal --> sBarWork.signal --> show_status_bar
            self.sBarWork.statusBarValue.connect(self.dns_work.trigger_tip)
            self.dns_work.trigger_tip.connect(self.show_status_bar)
            self.dns_work.start()
            self.dns_work.trigger_subdomains.connect(self.show_dns_result)

    def show_spider_result(self, subdomains: list):
        # 存储爬虫模块结果以便导出
        self.spider_subdomains.extend(subdomains)
        self.itemmodel_1.setStringList(subdomains)

    def show_dns_result(self, subdomains: list):
        # 存储DNS解析模块结果以便导出
        self.dns_subdomains.extend(subdomains)
        self.itemmodel_1.setStringList(subdomains)

    def show_status_bar(self, tip):
        if tip == "start":
            self.statusbar.showMessage("Spider or Dns resolution are running...")
        if tip == "finish":
            self.statusbar.showMessage("Spider or Dns resolution are finished!")

    def export_results_to_file(self):
        other_subdomains = self.spider_subdomains + self.dns_subdomains
        other_subdomains = deduplicate.remove_duplicate_data(other_subdomains)
        try:
            file_name = self.export_result_window.getSaveFileName(self, '导出结果')[0]
            with open(file_name, 'a+') as fp:
                fp.write("----------------Brute results:-------------------\n")
                for subdomain in self.brute_subdomains:
                    fp.write(subdomain+'\n')
                fp.write("-------------Spider or DNS resolution results:---------\n")
                for subdomain in other_subdomains:
                    fp.write(subdomain+'\n')
        except:
            pass



if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())
