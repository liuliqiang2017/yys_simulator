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
        self.location = self.speed # 在行动条上的初始位置
        self.team = None
        self.enemy = None
        self.status_buffs = [] # 和自身属性有关的buff列表
        self.skills = []
        self.passive_skills = []
        self.immune = False # 免疫负面状态
        self.run_times = 0 # 行动次数
        self.damage_out = 0 # 伤害输出
        self.show_time = 0 # 动画时间
        self.set_base_data()
        self.reset_extra_status()

    def set_base_data(self):
        "式神的自带初始属性，由子类实现"
        raise NotImplementedError
    
    def reset_extra_status(self):
        "重置自身的附加属性"
        self.shield = 0
        self.extra_atk = 0
        self.extra_def = 0
        self.extra_speed = 0
        self.extra_cri = 0
        self.extra_criDM = 0
        self.atk_ratio = 1
        self.def_ratio = 1
        self.harm_ratio = 1
        self.damage_ratio = 1
        self.max_hp_ratio = 1
        self.speed_ratio = 1
        self.def_break = 0
        self.def_reduce = 1
        
    def is_alive(self):
        return True if self.hp > 0 else False
    
    def update_buff(self):
        "更新式神的buff"
        for buff in self.status_buffs:
            buff.layer_update()

