from functools import partial
import json

from my_Window import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets

from servant_set_dialog import MyDialog
from config import SERVANT_SOURCE

import images

class My_MainWindow(Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.servant_data = {}
        [self.init_sevrant_data(num) for num in range(1, 11)]

    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        super().setupUi(MainWindow)
        self.set_all_backgourd()
        self.set_trigger_connect()
        self.statusBar.showMessage('这里是状态栏...')
        

    def set_all_backgourd(self):
        "设置所有背景图片"
        self.set_bg_pic(self.MainWindow, ":/yys_bg.jpg")
        self.set_bg_pic(self.centralwidget, ":/bg_frame.png")
        self.set_bg_pic(self.vs_pic, ":/vs.png")
        self.set_bg_pic(self.team1_leader, ":/qingming.jpg")
        self.set_bg_pic(self.team2_leader, ":/guiwang.jpg")
        for i in range(1, 11):
            self.refresh_servant_display(i)

    def set_bg_pic(self, target, path):
        target.setAutoFillBackground(True)
        palette = QtGui.QPalette()
        palette.setBrush(target.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(path)))
        target.setPalette(palette)

    def set_trigger_connect(self):
        "设置所有的联动" 
        # 设置所有添加式神的联动
        for i in range(1, 11):
            eval("self.bt_add{0}.clicked.connect(partial(self.add_servant_to, {0}))".format(i))
        # 设置所有的删除式神联动
        for i in range(1, 11):
            eval("self.bt_remove{0}.clicked.connect(partial(self.remove_servant_from, {0}))".format(i))
        # 设置开始模拟的联动：
        self.start_sim.clicked.connect(self.start_to_run)
        # 设置菜单里的联动：
        self.start_simulator.triggered.connect(self.start_to_run)
        self.save_team_data.triggered.connect(self.save_data_to_json)
        self.load_team_data.triggered.connect(self.load_data_from_json)
        self.help_information.triggered.connect(self.show_help_information)
        self.soft_info.triggered.connect(self.show_soft_info)
        self.exit_program.triggered.connect(QtWidgets.qApp.quit)
        # 提交所有联动信息
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

    def add_servant_to(self, location_num):
        "在num指定的位置添加新式神"
        # TODO, 载入data时还需要改进
        # 弹出添加式神面板，如果有data了就载入，否则空面板
        if not self.servant_data[str(location_num)]["servant_cls"]:
            res = self.create_set_panel()
        else:
            res = self.create_set_panel(self.servant_data[str(location_num)])
        # 根据返回的data数据初始化相对位置的头像，存储data
        if res:
            self.servant_data[str(location_num)] = res
            self.refresh_servant_display(location_num)
        # 启用相对位置的删除按键
            self.statusBar.showMessage("添加式神{}成功！".format(res["servant_name"]))
            self.release_bt(location_num)
    
    def remove_servant_from(self, location_num):
        "在num指定的位置清除数据"
        # 清除数据, 刷新显示
        self.init_sevrant_data(location_num)
        self.refresh_servant_display(location_num)
        # 锁定自身按钮不可用
        self.lock_bt(location_num)

    def refresh_servant_display(self, location_num):
        # TODO 刷新的判断要智能
        if self.has_servant(location_num):
            self.set_head_pic(location_num)
            self.release_bt(location_num)
        else:
            # eval("self.label{}.setStyleSheet('border-image:url(:/wanted_nodata.jpg)')".format(location_num))
            self.set_head_pic(location_num)
            self.lock_bt(location_num)
    
    def get_head_pic(self, location_num):
        try:
            return SERVANT_SOURCE[self.servant_data[str(location_num)]["servant_cls"]]["head_pic"]
        except KeyError:
            return "wanted_nodata.jpg"
    
    def set_head_pic(self, location_num):
        path = ":/" + self.get_head_pic(location_num)
        target = eval("self.label" + str(location_num))
        self.set_bg_pic(target, path)
    
    def has_servant(self, location_num):
        return self.servant_data[str(location_num)]["servant_cls"]
    
    def get_servant_data(self, location_num):
        return self.servant_data[str(location_num)]
    
    
    def lock_bt(self, location_num):
        eval("self.bt_remove{}.setEnabled(False)".format(location_num))
        eval("self.bt_add{}.setText('添加式神')".format(location_num))
    
    def release_bt(self, location_num):
        eval("self.bt_remove{}.setEnabled(True)".format(location_num))
        eval("self.bt_add{}.setText('修改式神')".format(location_num))

    def init_sevrant_data(self, location_num):
        data =  dict(servant_cls=None,
                     servant_name="", 
                     servant_atk=0, 
                     servant_def=0, 
                     servant_speed=0, 
                     servant_hp=0, 
                     servant_cri=0,
                     servant_cridm=0,
                     servant_yuhun=None)

        self.servant_data[str(location_num)] = data

    def create_set_panel(self, data=None):
        panel = MyDialog()
        if data:
            panel.set_data(data)
        if panel.exec_():
            return panel.get_result()
    
    def start_to_run(self):
        "运行模拟"
        self.create_set_panel()
        # TODO 根据data中存储的数据生成式神
        # TODO 建立team1，team2 ， battle。
        # TODO battle初始化，添加两个team
        # TODO 开始执行模拟
        # TODO 处理返回的模拟结果，生成表格展示在弹出窗口

    def save_data_to_json(self):
        "把所有式神的data数据保存到json文件"
        
        # TODO 弹出窗口要求用户选择存储位置
        fileName = QtWidgets.QFileDialog.getSaveFileName(None,
                                       r'创建队伍信息并保存',
                                       r'yys_teamdata',
                                       r'JSON Files(*.json)')
        with open(fileName[0], "w") as f_obj:
            json.dump(self.servant_data, f_obj)
        self.statusBar.showMessage("保存队伍成功")
        # TODO 保存文件，默认文件名yys_teamdata.json
        # TODO 成功保存就返回
    
    def load_data_from_json(self):
        "读取数据"
        # TODO 弹出窗口要求用户选择文件
        fileName = QtWidgets.QFileDialog.getOpenFileName(None,
                               r'创建队伍信息并保存',
                               r'yys_teamdata',
                               r'JSON Files(*.json)')
        with open(fileName[0], "r") as f_obj:
            self.servant_data = json.load(f_obj)
        # TODO 验证文件有效性
        # 读取json，覆盖本身的data
        # 重新刷新所有位置的信息
        for i in range(1, 11):
            self.refresh_servant_display(i)

    def show_help_information(self):
        "使用帮助"
        # TODO 弹出窗口，显示使用帮助
    
    def show_soft_info(self):
        "软件信息"
        # TODO 弹出窗口，显示软件信息

if __name__ == "__main__":
    import sys
    import cgitb 
    cgitb.enable(format='text')

    app = QtWidgets.QApplication(sys.argv)

    widget = QtWidgets.QMainWindow(None)
    My_MainWindow().setupUi(widget)
    widget.show()

    sys.exit(app.exec_())
