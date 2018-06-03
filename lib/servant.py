"""
式神相关类， 包括式神数据类Servant_Data, 伤害统计类Statistic， 式神基类
"""
from collections import defaultdict
from random import choice

class MemberDead(Exception):
    "成员死亡异常"
    pass

class ServantData:
    "式神数据基类，从给定的参数字典初始化式神的属性"
    def __init__(self, owner):
        super().__init__()
        self.owner = owner
        self.set_extra_status()
    
    def set_servant_status(self, data_dict):
        self.max_hp = float(data_dict["hp"])
        self.hp = self.max_hp
        self.speed = float(data_dict["speed"])
        self.atk = float(data_dict["atk"])
        self.def_ = float(data_dict["def_"])
        self.cri = float(data_dict["cri"])
        self.criDM = float(data_dict["criDM"])

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
    
    def hp_change(self, num):
        self.hp += num
        if self.hp < 0:
            self.hp = 0
        elif self.hp > self.get_max_hp():
            self.hp = self.get_max_hp()
    
    def get_speed(self):
        return self.speed + self.extra_speed

    def get_max_hp(self):
        return self.max_hp + self.base_max_hp * self.max_hp_ratio
    
    def get_hp_percent(self):
        return self.hp / self.get_max_hp()

    def change_damage_ratio(self, ratio_num):
        "改变攻击伤害比率"
        self.damage_ratio += ratio_num

    def change_hurt_ratio(self, ratio_num):
        "改变承伤比率"
        self.harm_ratio += ratio_num
    
    def change_atk_ratio(self, ratio_num):
        "改变基础攻击力"
        self.atk_ratio += ratio_num
    
    def change_def_ratio(self, ratio_num):
        "改变基础防御力"
        self.def_ratio += ratio_num

# TODO 式神被动御魂管理类
class PassiveManage:
    "被动，御魂等管理类"
    def __init__(self):
        super().__init__()
        self.pre_round = []
        self.post_round = []
        self.pre_skill = []
        self.post_skill = []
        self.by_hit = []

    def add(self, passive):
        self.__dict__[passive.position].append(passive)
    
    def remove(self, passive):
        try:
            self.__dict__[passive.position].remove(passive)
        except ValueError:
            pass
    
    def stimulate(self, target, position):
        for each in position:
            each.action(target)

    
    def action_pre_round(self, target):
        self.stimulate(target, self.pre_round)

    def action_post_round(self, target):
        self.stimulate(target, self.post_round)

    def action_pre_skill(self, target):
        self.stimulate(target, self.pre_skill)

    def action_post_skill(self, target):
        self.stimulate(target, self.post_skill)

    def action_by_hit(self, target):
        self.stimulate(target, self.by_hit)

class ServantPassive(PassiveManage):
    "式神被动"
    pass

class ServantYuHun(PassiveManage):
    "式神御魂"
    pass

class ServantHelper(PassiveManage):
    "式神的其他触发，比如记仇，土蜘蛛等"
    pass

class Statistic:

    "伤害统计类"
    def __init__(self, owner):
        self.record = dict(
            name=owner.name,
            round=0,
            show_time=0.0,
            skill_times=defaultdict(int),
            total_damage=0,
            max_damage=0,
            skill_damage=defaultdict(float),
            damage_defender=defaultdict(float)
        )
    
    def recorder_add_damage(self, damage):
        self.record["total_damage"] += damage.val
        self.record["skill_damage"][damage.name] += damage.val
        self.record["damage_defender"][damage.defer.name] += damage.val
        if self.record["max_damage"] < damage.val:
            self.record["max_damage"] = damage.val
    
    def recorder_add_skill(self, skill_name):
        self.record["skill_times"][skill_name] += 1
    
    def recorder_add_round(self, num=1):
        self.record["round"] += num
    
    def recorder_add_showtime(self, time):
        self.record["show_time"] += time
    
    def recorder_get_result(self):
        return self.record   


class baseServant:
    "式神基类"

    def __init__(self, data_dict):
        super().__init__()
        self.data_dict = data_dict
        self.name = data_dict.get("name", "未命名")
        self.status = ServantData(self)
        self.recorder = Statistic(self)
    
    def get_atk_data(self):
        return self.status.get_atk_data()
    
    def get_def_data(self):
        return self.status.get_def_data()
    
    def get_speed(self):
        return self.status.get_speed()

    def get_hp_percent(self):
        return self.status.get_hp_percent()
    
    def get_max_hp(self):
        return self.status.get_max_hp()
    
    def change_damage_ratio(self, ratio_num):
        return self.status.change_damage_ratio(ratio_num)
    
    def change_hurt_ratio(self, ratio_num):
        return self.status.change_hurt_ratio(ratio_num)
    
    def change_atk_ratio(self, ratio_num):
        return self.status.change_atk_ratio(ratio_num)

    def change_def_ratio(self, ratio_num):
        return self.status.change_def_ratio(ratio_num)
    
    def recorder_add_damage(self, damage):
        return self.recorder.recorder_add_damage(damage)

    def recorder_add_skill(self, skill_name):
        return self.recorder.recorder_add_skill(skill_name)

    def recorder_add_round(self):
        return self.recorder.recorder_add_round()

    def recorder_add_showtime(self, time):
        return self.recorder.recorder_add_showtime(time)

    def recorder_get_result(self):
        return self.recorder.recorder_get_result()

