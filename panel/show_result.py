
from PyQt5 import QtWidgets, QtCore
from .show_result_ui import Ui_Dialog
from .show_detail import ShowDetail

class ShowResult(QtWidgets.QDialog, Ui_Dialog):

    def __init__(self,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._data = {}
        # 对单元格添加点击事件
        self.table_total.cellActivated['int','int'].connect(self.check_cell_click)

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
        detail = ShowDetail()
        detail.set_data(data)
        detail.exec_()
