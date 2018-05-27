"""
式神相关类， 包括式神数据类Servant_Data, 式神技能类Servant_Skill, 伤害统计类Statistic， 式神基类
"""
from random import choice
import servant_base
from damage_ import NormalDamage

class Servant_Data:
    "式神数据基类，从给定的参数字典初始化式神的属性"
    def __init__(self, data_dict, owner):
        super().__init__()
        self.owner = owner
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
        self.base_max_hp = base_data["base_max_hp"]
    
    def set_extra_status(self):
        "重置自身的附加属性"
        self.shield = 0
        self.extra_atk = 0
        self.extra_def = 0
        self.extra_speed = 0
        self.extra_cri = 0
        self.extra_criDM = 0
        self.atk_ratio = 0
        self.def_ratio = 0
        self.harm_ratio = 1
        self.damage_ratio = 1
        self.max_hp_ratio = 0
        self.speed_ratio = 0
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
                    "atker" : self.owner
                    }
        return atk_data
    
    def get_speed(self):
        return self.speed + self.extra_speed

# TODO 式神技能类Servant_Skill

# TODO 伤害统计类Statistic

# TODO 式神基类

class Servant:
    "式神基类"
    def __init__(self, data_dict):
        super().__init__()
        self.data_dict = data_dict
        self.name = data_dict.get("name", "式神")
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

    def config(self, base=servant_base.BOSS_DUMMY):
        "由子类实现不同的初始设置，以下是个例子"
        # 初始化式神的基础属性
        self.status.set_base_data(base)
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

    def skill_1(self, targets, cost=0):
        self.team.energe_change(-cost)
        target = choice(targets)
        damage = NormalDamage(self)
        damage.name = "普通攻击"
        damage.factor = 1.25
        damage.set_defender(target)
        damage.run()
    
    def skill_2(self, targets, cost=0):
        pass
    
    def skill_3(self, targets, cost=3):
        self.team.energe_change(-cost)
        target = choice(targets)
        damage = NormalDamage(self)
        damage.name = "暴跳如雷"
        damage.factor = 3
        damage.set_defender(target)
        damage.run()
    
    def ai_act(self):
        "自动战斗时的ai，此处是最基础的3火开大ai"
        targets = self.enemy.alive_members()
        if targets:                
            if self.team.energe >= 3:
                self.skill_3(targets)
            else:
                self.skill_1(targets)
        
    def defend(self, damage):
        # 结算伤害
        self.damage_apply(damage)
        # TODO 受攻击后的被动触发判定
    
    def damage_apply(self, damage):
        self.status.hp -= damage.val
        print("{}对{}发动{}，造成{}伤害".format(damage.atker.name, damage.defer.name, damage.name, damage.val))
        print("{}的剩余血量是{}".format(self.name, self.status.hp))
    





