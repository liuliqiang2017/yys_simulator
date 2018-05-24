"""
式神类，包括玩家式神，阴阳师，木桩, 式神类基本上是个数据容器，存储了式神的各种属性。
提供以下几个方法，用于获取式神的当前攻击属性，当前防御属性等。
"""
import random

class baseServant:
    "式神基类，从给定的参数字典初始化式神的属性"
    def __init__(self, data_dict):
        super().__init__()
        self.name = data_dict.get("name", "式神")
        self.max_hp = data_dict["hp"]
        self.hp = self.max_hp
        self.speed = data_dict["speed"]
        self.atk = data_dict["atk"]
        self.def_ = data_dict["def_"]
        self.cri = data_dict["cri"]
        self.criDM = data_dict["criDM"]
        self.location = self.speed
        self.team = None
        self.enemy = None
        self.buffs = []
        self.skill = []
        self.passive_skill = []
        self.run_times = 0 # 行动次数
        self.damage_out = 0 # 伤害输出
        self.show_time = 0 # 动画时间
        self.set_base_data()
        self.reset_extra_status()

    def set_base_data(self):
        "式神的初始属性，由子类实现"
        raise NotImplementedError
    
    def reset_extra_status(self):
        "重置自身的附加属性，用于结算buff效果时"
        raise NotImplementedError
        
    def is_alive(self):
        return True if self.hp > 0 else False
    
    def add_buff(self, buff):
        self.buffs.append(buff)
        if buff.classify == 1:
            self.update_extra_status()
    
    def del_buff(self, buff):
        self.buffs.remove(buff)
        if buff.classify == 1:
            self.update_extra_status()
    
    def get_buff(self, *, classify):
        "从式神的buff列表中获取指定分类的buff，并按优先级排列"
        res = [buff for buff in self.buffs if buff.classify == classify]
        res.sort(key=lambda x: x.priority)
        return res
    
    def update_buff(self):
        "更新式神的buff"
        for buff in self.get_buff(classify=1):
            buff.layer_change()

    def update_extra_status(self):
        "更新式神的附加属性"
        self.reset_extra_status
        for buff in self.get_buff(classify=1):
            buff.valid(self)

