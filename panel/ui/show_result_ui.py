# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\show_result.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(500, 300)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        Dialog.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.widget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_total = QtWidgets.QWidget()
        self.tab_total.setObjectName("tab_total")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_total)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.table_total = QtWidgets.QTableWidget(self.tab_total)
        self.table_total.setRowCount(0)
        self.table_total.setObjectName("table_total")
        self.table_total.setColumnCount(5)
        self.table_total.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        item = QtWidgets.QTableWidgetItem()
        self.table_total.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_total.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_total.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_total.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_total.setHorizontalHeaderItem(4, item)
        self.verticalLayout_3.addWidget(self.table_total)
        self.tabWidget.addTab(self.tab_total, "")
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.verticalLayout.addWidget(self.widget)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.buttonBox.setFont(font)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "模拟结果"))
        item = self.table_total.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "式神"))
        item = self.table_total.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "总回合"))
        item = self.table_total.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "总伤害"))
        item = self.table_total.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "动画时间"))
        item = self.table_total.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", "最大伤害"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_total), _translate("Dialog", "战斗概况-双击式神名字显示详细信息"))

