from .servant_set_ui import Ui_Dialog
from PyQt5 import QtWidgets
from .config import SERVANT_SOURCE, YUHUN_SOURCE

class ServantSet(QtWidgets.QDialog, Ui_Dialog):

    def __init__(self,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.set_combobox()

    def get_result(self):
        data =  dict(servant_cls=self.servant_cls.currentText(),
                     servant_name=self.servant_name.text(), 
                     servant_atk=self.servant_atk.text(), 
                     servant_def=self.servant_def.text(), 
                     servant_speed=self.servant_speed.text(), 
                     servant_hp=self.servant_hp.text(), 
                     servant_cri=self.servant_cri.text(),
                     servant_cridm=self.servant_cridm.text(),
                     servant_yuhun=self.servant_yuhun.currentText())
        return data

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
        self.servant_cls.setCurrentIndex(SERVANT_SOURCE[data["servant_cls"]]["cls_index"])
        self.servant_name.setText(data["servant_name"])
        self.servant_atk.setText(data["servant_atk"])
        self.servant_def.setText(data["servant_def"])
        self.servant_hp.setText(data["servant_hp"])
        self.servant_speed.setText(data["servant_speed"])
        self.servant_cri.setText(data["servant_cri"])
        self.servant_cridm.setText(data["servant_cridm"])
        self.servant_yuhun.setCurrentIndex(YUHUN_SOURCE[data["servant_yuhun"]]["cls_index"])

    def set_combobox(self):
        for key in SERVANT_SOURCE.keys():
            self.servant_cls.addItem(key)
        for key in YUHUN_SOURCE.keys():
            self.servant_yuhun.addItem(key)


