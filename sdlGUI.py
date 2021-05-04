# @Author: chesterblue
# @File Name:sdlGUI.py

import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from Gui.gui import *
from Gui.GThread import *


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        # listview数据存储
        self.itemmodel = QtCore.QStringListModel(self)
        self.listView.setModel(self.itemmodel)

        # 读取字典目录下所有字典名
        self.get_all_file_name()

        # start按钮绑定多线程槽函数，执行任务
        self.pushButton.clicked.connect(self.execute)

    def execute(self):
        # 获取用户输入的domain值
        self.getDomain()
        # 获取用户在comboBox选择的字典名
        self.getDictname()
        # 实例化线程对象
        self.work = GThreadBrute(self.domain,self.dict)
        # 启动线程
        self.work.start()
        # 线程自定义信号连接的槽函数
        self.work.trigger.connect(self.addUrl)

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
        self.dict = "./dict/"+self.comboBox.currentText()

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





if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())