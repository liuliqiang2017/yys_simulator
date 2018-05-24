"""
式神类，包括玩家式神，阴阳师，木桩, 式神类基本上是个数据容器，存储了式神的各种属性。
提供以下几个方法，用于获取式神的当前攻击属性，当前防御属性等。
"""
import random
from damage import NormalDamage

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
        return self.hp > 0
    
    def update_buff(self):
        "更新式神的buff"
        for buff in self.status_buffs:
            buff.layer_update()

    def move(self):
        if self.is_alive():
            self.location += (self.speed * self.speed_ratio + self.extra_speed)

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
        atk_data = {"atker" : self,
                    "atk" : self.atk * self.atk_ratio + self.extra_atk,
                    "damage_ratio" : self.damage_ratio,
                    "def_break" : self.def_break,
                    "def_reduce" : self.def_reduce,
                    "cri" : self.cri + self.extra_cri,
                    "criDM" : self.criDM + self.extra_criDM,
                    "factor": 1,
                    "act_pre_hit" : [],
                    "act_when_hit" : [],
                    "act_after_hit" : [],
                    }
        return atk_data
    
    def defend(self, damage):
        # TODO 受攻击前的被动触发判定
        # TODO 被攻击时的被动触发判定
        # 结算攻击效果
        damage.set_defender(self)       
        self.damage_apply(damage.get_result())
        # TODO 受攻击后的被动触发判定
    
    def damage_apply(self, damage):
        self.hp -= damage.val
        print("{}对{}发动{}，造成{}伤害".format(damage.atker.name, damage.defer.name, damage.name, damage.val))
        print("{}的剩余血量是{}".format(self.name, self.hp))
    
    def act_ai(self):
        if self.team.energe >= 3:
            target = self.choose()
            self.skill_3(target)
        else:
            target = self.choose()
            self.skill_1(target)
    
    def skill_1(self, target, cost=0):
        self.team.energe_change(-cost)
        atk_dict = self.get_atk_data()
        atk_dict["name"] = "普通攻击"
        damage = NormalDamage(atk_dict)
        target.defend(damage)

    def skill_2(self):
        pass
    
    def skill_3(self, target, cost=3):
        self.team.energe_change(-cost)
        atk_dict = self.get_atk_data()
        atk_dict["factor"] = 3
        atk_dict["name"] = "暴跳如雷"
        damage = NormalDamage(atk_dict)
        target.defend(damage)

    def choose(self):
        target_list = self.enemy.alive_members()
        return random.choice(target_list)