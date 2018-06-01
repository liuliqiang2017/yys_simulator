
from .show_detail_ui import Ui_Dialog
from PyQt5 import QtWidgets, QtCore

class ShowDetail(QtWidgets.QDialog, Ui_Dialog):

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

