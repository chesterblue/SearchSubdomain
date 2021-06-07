# @Author: chesterblue
# @File Name:gui.py

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets, Qt

IconImg = "./img/logo.png"

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(802, 597)
        # 禁止最大化按钮
        MainWindow.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint|QtCore.Qt.WindowCloseButtonHint)
        # 禁止拉伸窗口大小
        MainWindow.setFixedSize(MainWindow.width(), MainWindow.height())
        # 设置窗口图标
        MainWindow.setWindowIcon(QtGui.QIcon(IconImg))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(11, 22, 771, 521))
        self.widget.setObjectName("widget")
        # 垂直布局
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        # 水平布局
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        # 顶部：lineEdit、label、spinBox、comboBox、button -------------start:top-----------------------------------
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.comboBox = QtWidgets.QComboBox(self.widget)
        self.comboBox.setEditable(False)
        self.comboBox.setCurrentText("")
        self.comboBox.setIconSize(QtCore.QSize(16, 16))
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout.addWidget(self.comboBox)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.spinBox = QtWidgets.QSpinBox(self.widget)
        self.spinBox.setProperty("value", 5)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout.addWidget(self.spinBox)
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        # 第一层水平布局添加到总体的垂直布局中
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        # ---------------------------------------------------------end:top------------------------------------------
        # progressBar、checkBox、listView-------------------------start:middle---------------------------------------
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.progressBar = QtWidgets.QProgressBar(self.widget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        # checkBox水平布局区域-----------------------------start-------------------------------
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.brute_checkBox = QtWidgets.QCheckBox()
        self.brute_checkBox.setObjectName("brute_checkBox")
        self.horizontalLayout_2.addWidget(self.brute_checkBox)
        self.checkBox_1 = QtWidgets.QCheckBox()
        self.checkBox_1.setObjectName("checkBox_1")
        self.horizontalLayout_2.addWidget(self.checkBox_1)
        self.checkBox_2 = QtWidgets.QCheckBox()
        self.checkBox_2.setObjectName("checkBox_2")
        self.horizontalLayout_2.addWidget(self.checkBox_2)
        self.checkBox_3 = QtWidgets.QCheckBox()
        self.checkBox_3.setObjectName("checkBox_3")
        self.horizontalLayout_2.addWidget(self.checkBox_3)
        self.checkBox_4 = QtWidgets.QCheckBox()
        self.checkBox_4.setObjectName("checkBox_4")
        self.horizontalLayout_2.addWidget(self.checkBox_4)
        # 四个checkBox的水平布局添加到和进度条组成的垂直布局中
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        # checkBox水平布局区域-----------------------------end-------------------------------
        # 两个listView水平布局区域--------------------------start--------------------------------
        self.horizontalLayout_1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_1.setObjectName("horizontalLayout_1")
        self.listView = QtWidgets.QListView(self.widget)
        self.listView.setObjectName("listView")
        self.horizontalLayout_1.addWidget(self.listView)
        self.listView_1 = QtWidgets.QListView(self.widget)
        self.listView_1.setObjectName("listView")
        self.horizontalLayout_1.addWidget(self.listView_1)
        # 两个listView水平布局区域--------------------------end--------------------------------
        # 两个水平分布的listView添加到和进度条组成的垂直布局中
        self.verticalLayout.addLayout(self.horizontalLayout_1)
        # 进度条、listView添加到总体的垂直布局中
        self.verticalLayout_2.addLayout(self.verticalLayout)
        # ----------------------------------------end:middle----------------------------------------------------------
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 802, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        # -------------------------------start:settings menu-----------------------------------------------------------
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.actionproxy = QtWidgets.QAction(MainWindow)
        self.actionproxy.setObjectName("actionproxy")
        self.actionAPI_Key = QtWidgets.QAction(MainWindow)
        self.actionAPI_Key.setObjectName("actionAPI_Key")
        self.menu.addAction(self.actionproxy)
        self.menu.addAction(self.actionAPI_Key)
        self.menubar.addAction(self.menu.menuAction())
        # ------------------------------end:settings menu--------------------------------------------------------------
        # ------------------------------start:tool menu-------------------------------------------------------------
        self.tool_menu = QtWidgets.QMenu(self.menubar)
        self.tool_menu.setObjectName("toolMenu")
        self.actionexport = QtWidgets.QAction(MainWindow)
        self.actionexport.setObjectName("actionexport")
        self.tool_menu.addAction(self.actionexport)
        self.actionportscan = QtWidgets.QAction(MainWindow)
        self.actionportscan.setObjectName("actionportscan")
        self.tool_menu.addAction(self.actionportscan)
        self.menubar.addAction(self.tool_menu.menuAction())

        # -------------------------------end:tool menu--------------------------------------------------------------
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Subdomain lookup V1.7.4"))
        self.label.setText(_translate("MainWindow", "站点"))
        self.label_3.setText(_translate("MainWindow", "字典"))
        self.comboBox.setPlaceholderText(_translate("MainWindow", "common.txt"))
        self.label_2.setText(_translate("MainWindow", "线程"))
        self.pushButton.setText(_translate("MainWindow", "Start"))
        self.brute_checkBox.setText(_translate("MainWindow", "Brute"))
        self.checkBox_1.setText(_translate("MainWindow", "Baidu"))
        self.checkBox_2.setText(_translate("MainWindow", "Bing"))
        self.checkBox_3.setText(_translate("MainWindow", "Google"))
        self.checkBox_4.setText(_translate("MainWindow", "DNS resolution"))
        self.menu.setTitle(_translate("MainWindow", "设置"))
        self.actionproxy.setText(_translate("MainWindow", "代理"))
        self.actionAPI_Key.setText(_translate("MainWindow", "API Key"))
        self.tool_menu.setTitle(_translate("MainWindow", "工具"))
        self.actionexport.setText(_translate("MainWindow", "导出结果"))
        self.actionportscan.setText(_translate("MainWindow", "端口扫描"))


class Ui_SetProxy(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(410, 296)
        # 禁止最大化按钮
        Dialog.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
        # 禁止拉伸窗口大小
        Dialog.setFixedSize(Dialog.width(), Dialog.height())
        # 设置窗口图标
        Dialog.setWindowIcon(QtGui.QIcon(IconImg))
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 100, 351, 61))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        # self.prompt_label = QtWidgets.QLabel(self.layoutWidget)
        # self.prompt_label.setObjectName("prompt_label")
        # self.gridLayout.addWidget(self.prompt_label, 1, 0, 1, 1)
        self.port_label = QtWidgets.QLabel(self.layoutWidget)
        self.port_label.setAlignment(QtCore.Qt.AlignCenter)
        self.port_label.setObjectName("port_label")
        self.gridLayout.addWidget(self.port_label, 0, 2, 1, 1)
        self.http_port = QtWidgets.QSpinBox(self.layoutWidget)
        self.http_port.setMaximum(65535)
        self.http_port.setObjectName("http_port")
        self.gridLayout.addWidget(self.http_port, 1, 2, 1, 1)
        self.http_address = QtWidgets.QLineEdit(self.layoutWidget)
        self.http_address.setObjectName("http_address")
        self.gridLayout.addWidget(self.http_address, 1, 1, 1, 1)
        self.ip_label = QtWidgets.QLabel(self.layoutWidget)
        self.ip_label.setAlignment(QtCore.Qt.AlignCenter)
        self.ip_label.setObjectName("ip_label")
        self.gridLayout.addWidget(self.ip_label, 0, 1, 1, 1)
        self.testProxyButton = QtWidgets.QPushButton(Dialog)
        self.testProxyButton.setGeometry(QtCore.QRect(30, 200, 75, 23))
        self.testProxyButton.setObjectName("testButton")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(40, 30, 301, 51))
        self.groupBox.setObjectName("groupBox")
        self.socks5_radioButton = QtWidgets.QRadioButton(self.groupBox)
        self.socks5_radioButton.setGeometry(QtCore.QRect(180, 20, 89, 16))
        self.socks5_radioButton.setObjectName("socks5_radioButton")
        self.http_radioButton = QtWidgets.QRadioButton(self.groupBox)
        self.http_radioButton.setGeometry(QtCore.QRect(40, 20, 89, 16))
        self.http_radioButton.setObjectName("http_radioButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.http_address, self.http_port)
        Dialog.setTabOrder(self.http_port, self.testProxyButton)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        # self.prompt_label.setText(_translate("Dialog", "HTTP:"))
        self.port_label.setText(_translate("Dialog", "port"))
        self.ip_label.setText(_translate("Dialog", "user:pass@ip/domain name"))
        self.testProxyButton.setText(_translate("Dialog", "Test"))
        self.groupBox.setTitle(_translate("Dialog", "Model/模式"))
        self.socks5_radioButton.setText(_translate("Dialog", "socks5"))
        self.http_radioButton.setText(_translate("Dialog", "http"))


class Ui_TestProxy(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(379, 160)
        # 禁止最大化按钮
        Dialog.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
        # 禁止拉伸窗口大小
        Dialog.setFixedSize(Dialog.width(), Dialog.height())
        # 设置窗口图标
        Dialog.setWindowIcon(QtGui.QIcon(IconImg))
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 120, 331, 31))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(20, 40, 321, 61))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "测试代理"))
        self.label_2.setText(_translate("Dialog", "输入任意URL以检查代理"))
        self.label.setText(_translate("Dialog", "链接/URL"))
        self.lineEdit.setText(_translate("Dialog", "http://"))


class Ui_SetAPI(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        # 禁止最大化按钮
        Dialog.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
        # 禁止拉伸窗口大小
        Dialog.setFixedSize(Dialog.width(), Dialog.height())
        # 设置窗口图标
        Dialog.setWindowIcon(QtGui.QIcon(IconImg))
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(50, 60, 301, 111))
        self.groupBox.setObjectName("groupBox")
        self.widget = QtWidgets.QWidget(self.groupBox)
        self.widget.setGeometry(QtCore.QRect(10, 40, 281, 21))
        self.widget.setObjectName("widget")
        self.formLayout = QtWidgets.QFormLayout(self.widget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.virus_api_key_value = QtWidgets.QLineEdit(self.widget)
        self.virus_api_key_value.setObjectName("virus_api_key_value")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.virus_api_key_value)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "API Key"))
        self.groupBox.setTitle(_translate("Dialog", "API Key"))
        self.label.setText(_translate("Dialog", "VirusTotal:"))


class Ui_portScan(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(732, 418)
        # 禁止最大化按钮
        Form.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
        # 禁止拉伸窗口大小
        Form.setFixedSize(Form.width(), Form.height())
        # 设置窗口图标
        Form.setWindowIcon(QtGui.QIcon(IconImg))
        self.domain_lineEdit = QtWidgets.QLineEdit(Form)
        self.domain_lineEdit.setGeometry(QtCore.QRect(30, 50, 251, 20))
        self.domain_lineEdit.setObjectName("domain_lineEdit")
        self.result_tableWidget = QtWidgets.QTableWidget(Form)
        self.result_tableWidget.setGeometry(QtCore.QRect(330, 20, 371, 381))
        self.result_tableWidget.setObjectName("result_tableWidget")
        self.result_tableWidget.setColumnCount(2)
        self.result_tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.result_tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.result_tableWidget.setHorizontalHeaderItem(1, item)
        self.port_textBrowser = QtWidgets.QTextBrowser(Form)
        self.port_textBrowser.setGeometry(QtCore.QRect(30, 110, 251, 141))
        self.port_textBrowser.setReadOnly(False)
        self.port_textBrowser.setObjectName("port_textBrowser")
        self.buttonBox = QtWidgets.QDialogButtonBox(Form)
        self.buttonBox.setGeometry(QtCore.QRect(120, 290, 161, 31))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.domain_label = QtWidgets.QLabel(Form)
        self.domain_label.setGeometry(QtCore.QRect(30, 20, 81, 16))
        self.domain_label.setObjectName("domain_label")
        self.port_label = QtWidgets.QLabel(Form)
        self.port_label.setGeometry(QtCore.QRect(30, 80, 54, 12))
        self.port_label.setObjectName("port_label")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "端口扫描"))
        item = self.result_tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "port"))
        item = self.result_tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Service"))
        # self.port_textBrowser.setHtml(_translate("Form", "80,8080,445,21,22,23,6379,3306,1521,1433,6379"))
        self.domain_label.setText(_translate("Form", "Domain Name"))
        self.port_label.setText(_translate("Form", "port"))
        self.port_textBrowser.setText("80,8080,445,21,22,23,6379,3306,1521,1433")
        # self.port_textBrowser.setTextCursor(Qt.CrossCursor)