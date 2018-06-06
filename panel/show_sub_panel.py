from PyQt5 import QtWidgets, QtGui, QtCore
from .config import SERVANT_SOURCE, YUHUN_SOURCE, YUHUN_01_SOURCE
from .ui import show_help_info_ui, servant_set_ui, show_detail_ui, show_result_ui, show_soft_info_ui

class ShowHelp(QtWidgets.QDialog, show_help_info_ui.Ui_Dialog):

    def __init__(self,parent=None):
        super().__init__(parent)
        self.setupUi(self)

class ShowSoft(QtWidgets.QDialog, show_soft_info_ui.Ui_Dialog):

    def __init__(self,parent=None):
        super().__init__(parent)
        self.setupUi(self)

class ServantSet(QtWidgets.QDialog, servant_set_ui.Ui_Dialog):

    def __init__(self,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.set_combobox()
        self.input_limit()

    def get_result(self):
        data =  dict(servant_cls=self.servant_cls.currentText(),
                     servant_name=self.servant_name.text(), 
                     servant_atk=self.servant_atk.text(), 
                     servant_def=self.servant_def.text(), 
                     servant_speed=self.servant_speed.text(), 
                     servant_hp=self.servant_hp.text(), 
                     servant_cri=self.servant_cri.text(),
                     servant_cridm=self.servant_cridm.text(),
                     servant_yuhun=self.servant_yuhun.currentText(),
                     servant_yuhun_01=self.servant_yuhun_01.currentText()
                     )
        return data
    
    def input_limit(self):
        reg = QtCore.QRegExp(r"^\d+(\.\d+)?$")
        validator = QtGui.QRegExpValidator(reg)
        self.servant_atk.setValidator(validator)
        self.servant_def.setValidator(validator)
        self.servant_hp.setValidator(validator)
        self.servant_speed.setValidator(validator)
        self.servant_cri.setValidator(validator)
        self.servant_cridm.setValidator(validator)


    def accept(self):
        if self.check_data():
            super().accept()
        else:
            self.label_9.setText("     请检查是否所有选项都输入有效的数据！")

    def check_data(self):
        for each in self.get_result().values():
            if not each:
                return False
        return True

    def set_data(self, data):
        self.servant_cls.setCurrentIndex(self.servant_cls.findText(data["servant_cls"]))
        self.servant_name.setText(data["servant_name"])
        self.servant_atk.setText(data["servant_atk"])
        self.servant_def.setText(data["servant_def"])
        self.servant_hp.setText(data["servant_hp"])
        self.servant_speed.setText(data["servant_speed"])
        self.servant_cri.setText(data["servant_cri"])
        self.servant_cridm.setText(data["servant_cridm"])
        self.servant_yuhun.setCurrentIndex(self.servant_yuhun.findText(data["servant_yuhun"]))
        if "servant_yuhun_01" in data:
            self.servant_yuhun_01.setCurrentIndex(self.servant_yuhun_01.findText(data["servant_yuhun_01"]))

    def set_combobox(self):
        self.servant_cls.addItems(SERVANT_SOURCE.keys())
        self.servant_yuhun.addItems(YUHUN_SOURCE.keys())
        self.servant_yuhun_01.addItems(YUHUN_01_SOURCE.keys())

class ShowDetail(QtWidgets.QDialog, show_detail_ui.Ui_Dialog):

    def __init__(self,parent=None):
        super().__init__(parent)
        self.setupUi(self)
    
    def set_data(self, data_dict):
        self.data = data_dict
        self.set_skill_damage()
        self.set_defend_damage()
    
    def set_skill_damage_one(self, key):
        table = self.table_skill_damage
        row = table.rowCount()
        table.setRowCount(row + 1)
        skill_times = self.data["skill_times"].get(key, 0)
        skill_damage = self.data["skill_damage"].get(key, 0)

        self.set_table_cell(table, key,  row, 0)
        self.set_table_cell(table, skill_times, row, 1)
        self.set_table_cell(table, skill_damage, row, 2)
    
    def set_skill_damage(self):
        for key in self.data["skill_times"].keys() | self.data["skill_damage"].keys():
            self.set_skill_damage_one(key)
        self.table_skill_damage.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    
    def set_defend_damage(self):
        for key, val in self.data["damage_defender"].items():
            self.set_defend_damage_one(key, val)
        self.table_defend_damage.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
    
    def set_defend_damage_one(self, key, val):
        table = self.table_defend_damage
        row = table.rowCount()
        table.setRowCount(row + 1)

        self.set_table_cell(table, key, row, 0)
        self.set_table_cell(table, val, row, 1)
    
    def set_table_cell(self, table, data, row, col):
        if isinstance(data, float):
            data = round(data)
        newItem = QtWidgets.QTableWidgetItem(str(data))
        newItem.setTextAlignment(QtCore.Qt.AlignCenter)
        table.setItem(row, col, newItem)

class ShowResult(QtWidgets.QDialog, show_result_ui.Ui_Dialog):

    def __init__(self,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._data = {}
        # 对单元格添加点击事件
        self.table_total.cellActivated['int','int'].connect(self.check_cell_click)
        self.table_total.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        
    def set_table_row(self, data_dict):
        row = self.table_total.rowCount()
        self.table_total.setRowCount(row + 1)
        # 设置各个单元格的值
        self.set_table_cell(data_dict["name"], row, 0)
        self.set_table_cell(data_dict["round"], row, 1)
        self.set_table_cell(data_dict["total_damage"], row, 2)
        self.set_table_cell(data_dict["show_time"], row, 3)
        self.set_table_cell(data_dict["max_damage"], row, 4)
        # 将data_dict存储，以备后用
        self._data[row] = data_dict

    def set_table_cell(self, data, row, col):
        if isinstance(data, float):
            data = round(data)
        newItem = QtWidgets.QTableWidgetItem(str(data))
        newItem.setTextAlignment(QtCore.Qt.AlignCenter)
        self.table_total.setItem(row, col, newItem)
    
    def check_cell_click(self):
        # 获取选中的格子的列
        col = self.table_total.currentColumn()
        row = self.table_total.currentRow()
        # 根据格子的col来显示detail
        if col == 0:
            self.show_damage_detail(row)
    
    def show_damage_detail(self, row):
        data = self._data[row]
        detail = ShowDetail(self)
        detail.set_data(data)
        detail.exec_()
