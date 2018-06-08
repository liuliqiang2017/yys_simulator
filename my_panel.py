from functools import partial
import json

from panel.ui.main_Window_ui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets

from panel.show_sub_panel import ServantSet, ShowResult, ShowHelp ,ShowSoft
from panel.config import SERVANT_SOURCE

from lib.battle import Simulate

from resource import images

class base_MainWindow(Ui_MainWindow):

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
        my_icon = QtGui.QIcon(":/vs.png")
        MainWindow.setWindowIcon(my_icon)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        MainWindow.setFont(font)
        self.set_css()
    
    def init_sevrant_data(self, location_num):
        raise NotImplementedError
    
    def set_all_backgourd(self):
        raise NotImplementedError
    
    def set_css(self):
        with open('./panel/css.qss', 'r', encoding='utf-8') as q:
            self.centralwidget.setStyleSheet(q.read())
    
    def set_trigger_connect(self):
        raise NotImplementedError
    
    def set_bg_pic(self, target, path):
        target.setAutoFillBackground(True)
        palette = QtGui.QPalette()
        palette.setBrush(target.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(path)))
        target.setPalette(palette)

    def get_head_pic(self, location_num):
        try:
            return SERVANT_SOURCE[self.servant_data[str(location_num)]["servant_cls"]]["head_pic"]
        except KeyError:
            return "wanted_nodata.jpg"
    
    def set_head_pic(self, location_num):
        path = ":/" + self.get_head_pic(location_num)
        target = getattr(self, "label" + str(location_num))
        self.set_bg_pic(target, path)
    
    def has_servant(self, location_num):
        return self.servant_data[str(location_num)]["servant_cls"]
    
    def get_servant_data(self, location_num):
        return self.servant_data[str(location_num)]    
    
    def lock_bt(self, location_num):
        getattr(self, "bt_remove" + str(location_num)).setEnabled(False)
        getattr(self, "bt_add" + str(location_num)).setText('添加式神')
    
    def release_bt(self, location_num):
        getattr(self, "bt_remove" + str(location_num)).setEnabled(True)
        getattr(self, "bt_add" + str(location_num)).setText('修改式神')
    



class My_MainWindow(base_MainWindow):        

    def set_all_backgourd(self):
        "设置所有背景图片"
        self.set_bg_pic(self.MainWindow, ":/yys_bg.jpg")
        self.set_bg_pic(self.centralwidget, ":/bg_frame.png")
        self.set_bg_pic(self.vs_pic, ":/vs.png")
        self.set_bg_pic(self.team1_leader, ":/qingming.jpg")
        self.set_bg_pic(self.team2_leader, ":/guiwang.jpg")
        for i in range(1, 11):
            self.refresh_servant_display(i)

    def set_trigger_connect(self):
        "设置所有的联动" 
        # 设置所有添加式神的联动
        for i in range(1, 11):
            getattr(self, "bt_add" + str(i)).clicked.connect(partial(self.add_servant_to, i))
        # 设置所有的删除式神联动
        for i in range(1, 11):
            getattr(self, "bt_remove" + str(i)).clicked.connect(partial(self.remove_servant_from, i))
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
        
        # 弹出添加式神面板，如果有data了就载入，否则空面板
        if not self.has_servant(location_num):
            res = self.create_set_panel()
        else:
            res = self.create_set_panel(self.servant_data[str(location_num)])
        # 根据返回的data数据初始化相对位置的头像，存储data
        if res:
            self.servant_data[str(location_num)] = res
            self.refresh_servant_display(location_num)
        # 启用相对位置的删除按键
            self.statusBar.showMessage("添加式神{}成功！".format(res["servant_cls"]))
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
            self.set_head_pic(location_num)
            self.lock_bt(location_num)

    def init_sevrant_data(self, location_num):
        "恢复式神数据到初始状态"
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
        panel = ServantSet(self.centralwidget)
        if data:
            panel.set_data(data)
        if panel.exec_():
            return panel.get_result()
    
    def start_to_run(self):
        "运行模拟"
        self.statusBar.showMessage("模拟开始,运算中...")
        simulator = Simulate(self.servant_data)
        sim = MyThread(simulator)
        sim.sim_over.connect(self.show_sim_result)
        sim.start()
        sim.wait()

    def show_sim_result(self, res_list):
        # 状态栏显示胜负
        if res_list[0] is None:
            self.statusBar.showMessage("成功模拟出结果,在{:.0f}秒内未分胜负".format(res_list[3]))
        else:
            self.statusBar.showMessage("成功模拟出结果,team{}获胜,总计用时{:.1f}秒".format(1 if res_list[0] else 2, res_list[3]))
        # res_list一共有3个元素，[0]是team1获胜的标志，[1]是team1的成员统计，[2]是team2的成员统计
        # TODO 用ui文件建立展示窗口实例
        result = ShowResult(self.centralwidget)
        # 遍历team1中的成员，将数据填充到对应的单元格，TODO 连接好trigger
        for each in res_list[1]:
            result.set_table_row(each)
        for each in res_list[2]:
            result.set_table_row(each)
        # 调用exec_()显示窗口
        result.exec_()



    def save_data_to_json(self):
        "把所有式神的data数据保存到json文件"
        
        # 弹出窗口要求用户选择存储位置
        fileName = QtWidgets.QFileDialog.getSaveFileName(None,
                                       r'创建队伍信息并保存',
                                       r'yys_teamdata',
                                       r'JSON Files(*.json)')
        # 保存文件，默认文件名yys_teamdata.json
        with open(fileName[0], "w") as f_obj:
            json.dump(self.servant_data, f_obj)

        # 状态栏提示
        self.statusBar.showMessage("保存队伍成功")

    
    def load_data_from_json(self):
        "读取数据"
        # 弹出窗口要求用户选择文件
        fileName = QtWidgets.QFileDialog.getOpenFileName(None,
                               r'创建队伍信息并保存',
                               r'yys_teamdata',
                               r'JSON Files(*.json)')
        with open(fileName[0], "r") as f_obj:
            try:
                data = json.load(f_obj)
            except json.decoder.JSONDecodeError:
                self.statusBar.showMessage("读取队伍失败，数据损坏")
                return
    
        if len(data) == 10:
            # 读取json，覆盖本身的data
            self.servant_data = data
            # 重新刷新所有位置的信息
            for i in range(1, 11):
                self.refresh_servant_display(i)
            self.statusBar.showMessage("读取队伍成功")
        else:
            self.statusBar.showMessage("读取队伍失败，数据损坏")

    def show_help_information(self):
        "使用帮助"
        ShowHelp(self.centralwidget).exec_()
    
    def show_soft_info(self):
        "软件信息"
        ShowSoft(self.centralwidget).exec_()

class MyThread(QtCore.QThread):

    sim_over = QtCore.pyqtSignal(list)

    def __init__(self, task):
        super().__init__()
        self.task = task

    def run(self):
        self.sim_over.emit(self.task.run())


if __name__ == "__main__":
    import sys
    import cgitb 
    cgitb.enable(format='text')

    app = QtWidgets.QApplication(sys.argv)

    widget = QtWidgets.QMainWindow(None)
    My_MainWindow().setupUi(widget)
    widget.show()

    sys.exit(app.exec_())
