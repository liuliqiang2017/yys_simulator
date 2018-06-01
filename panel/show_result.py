from .show_result_ui import Ui_Dialog
from PyQt5 import QtWidgets

class ShowResult(QtWidgets.QDialog, Ui_Dialog):

    def __init__(self,parent=None):
        super().__init__(parent)
        self.setupUi(self)

    def set_table_row(self, data_dict):
        row = self.table_total.rowCount()
        self.table_total.setRowCount(row + 1)
        self.set_table_cell(data_dict["name"], row, 0)
        self.set_table_cell(data_dict["round"], row, 1)
        self.set_table_cell(data_dict["total_damage"], row, 2)
        self.set_table_cell(data_dict["show_time"], row, 3)
        self.set_table_cell(data_dict["max_damage"], row, 4)

    def set_table_cell(self, data, row, col):
        if isinstance(data, float):
            data = round(data)
        newItem = QtWidgets.QTableWidgetItem(str(data))
        self.table_total.setItem(row, col, newItem)
    