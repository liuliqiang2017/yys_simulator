"""
式神相关类， 包括式神数据类Servant_Data, 式神技能类Servant_Skill, 伤害统计类Statistic， 式神基类
"""
import servant_base

class Servant_Data:
    "式神数据基类，从给定的参数字典初始化式神的属性"
    def __init__(self, data_dict, owner):
        super().__init__()
        self.owner = owner
        self.name = data_dict.get("name", "式神")
        self.max_hp = data_dict["hp"]
        self.hp = self.max_hp
        self.speed = data_dict["speed"]
        self.atk = data_dict["atk"]
        self.def_ = data_dict["def_"]
        self.cri = data_dict["cri"]
        self.criDM = data_dict["criDM"]

        self.set_extra_status()

    def set_base_data(self, base_data):
        "导入式神的基础属性"
        self.base_atk = base_data["base_atk"]
        self.base_def = base_data["base_def"]
        self.base_speed = base_data["base_speed"]
        self.base_cri = base_data["base_cri"]
        self.base_criDM = base_data["base_criDM"]
        self.base_max_hp = base_data["bace_max_hp"]
    
    def set_extra_status(self):
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

    def get_def_data(self):
        def_data = {"def" : self.def_,
                    "extra_def" : self.extra_def,
                    "def_ratio" : self.def_ratio,
                    "harm_ratio" : self.harm_ratio,
                    "shield": self.shield,
                    "hp": self.hp,
                    "max_hp": self.max_hp
                    }
        return def_data

    def get_atk_data(self):
        atk_data = {"atk" : self.base_atk * self.atk_ratio + self.extra_atk + self.atk,
                    "damage_ratio" : self.damage_ratio,
                    "def_break" : self.def_break,
                    "def_reduce" : self.def_reduce,
                    "cri" : self.cri + self.extra_cri,
                    "criDM" : self.criDM + self.extra_criDM,
                    "atiker" : self.owner
                    }
        return atk_data

# TODO 式神技能类Servant_Skill

# TODO 伤害统计类Statistic

# TODO 式神基类

class Servant:
    "式神基类"
    def __init__(self, data_dict):
        super().__init__()
        self.data_dict = data_dict
        self.status = Servant_Data(data_dict, self)
        self.location = self.status.speed
        self.immune = False
        self.team = None
        self.enemy = None
        self.arena = None
        self.status_buff = []
        self.trigger_pre_round = []
        self.trigger_post_round = []
        self.trigger_pre_skill = []
        self.trigger_post_skill = []
        self.trigger_by_hit = []
        self.config()

    def config(self):
        "由子类实现不同的初始设置，以下是个例子"
        # 初始化式神的基础属性
        self.status.set_base_data(servant_base.BOSS_DUMMY)
        # 设置式神的御魂
        for yh in self.data_dict["yuhun"]:
            yh().add(self)
        # 设置式神的被动
        for passive_skill in servant_base.BOSS_DUMMY["passive"]:
            passive_skill().add(self)
    
    def is_alive(self):
        return self.status.hp > 0
    
    def move(self, distance=None):
        self.location += distance if distance else self.status.speed + self.status.extra_speed

    





