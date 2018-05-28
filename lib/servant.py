"""
式神相关类， 包括式神数据类Servant_Data, 式神技能类Servant_Skill, 伤害统计类Statistic， 式神基类
"""
from collections import defaultdict
from random import choice
import servant_base
import skill_
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

    def get_max_hp(self):
        return self.max_hp + self.base_max_hp * self.max_hp_ratio
    
    def get_hp_percent(self):
        return self.hp / self.get_max_hp()

# TODO 式神技能类Servant_Skill

class Statistic:
    "伤害统计类"
    def __init__(self, owner):
        self.owner = owner
        self.record = defaultdict(int)
    
    def add_damage(self, damage):
        self.record["total_damage"] += damage.val
        self.record[damage.name] += damage.val
    
    def add_skill(self, skill_name, num=1):
        self.record[skill_name + "次数"] += 1
    
    def add_round(self, num=1):
        self.record["round"] += num
    
    def add_showtime(self, time):
        self.record["showtime"] += time
    
    def get_result(self):
        return self.record

class Servant:
    "式神基类"
    def __init__(self, data_dict):
        super().__init__()
        self.data_dict = data_dict
        self.name = data_dict.get("name", "未命名")
        self.status = Servant_Data(data_dict, self)
        self.recorder = Statistic(self)
        self.location = self.status.speed
        self.immune = False
        self.team = None
        self.enemy = None
        self.arena = None
        self.run_once = []
        self.status_buff = []
        self.trigger_pre_round = []
        self.trigger_post_round = []
        self.trigger_pre_skill = []
        self.trigger_post_skill = []
        self.trigger_by_hit = []

    def config(self, base=servant_base.BOSS_DUMMY):
        "由子类实现不同的初始设置，以下是个例子"
        # 初始化式神的基础属性
        self.status.set_base_data(base)
        # 设置式神的技能
        self.set_skills()
        # 设置式神的御魂
        for yh in self.data_dict["yuhun"]:
            yh(self).add(self)
        # 设置式神的被动
        for passive_skill in base["passive"]:
            passive_skill(self).add(self)
        # 使用开场运行一次的技能
        for each in self.run_once:
            each.action()
    
    def set_skills(self):
        self.skill_1 = skill_.ServantSkill1(self)
        self.skill_3 = skill_.ServantSkill3(self)
    
    def is_alive(self):
        return self.status.hp > 0
    
    def move(self, distance=None):
        self.location += distance if distance else self.status.get_speed()
    
    def ai_act(self):
        "自动战斗时的ai，此处是最基础的3火开大ai"
        targets = self.enemy.alive_members()
        if targets:                
            if self.team.energe >= self.skill_3.cost:
                self.skill_3(choice(targets))
            else:
                self.skill_1(choice(targets))
    
    def counter(self, target):
        "反击，默认用一技能反击"
        self.assist(target)
    
    def assist(self, target):
        "协战，默认用一技能协战"
        if target.is_alive():
            self.skill_1(target)
        else:
            if self.enemy.alive_members():
                self.skill_1(choice(self.enemy.alive_members()))
        
    def defend(self, damage):
        # 结算伤害
        self.damage_apply(damage)
        # 输出伤害信息，方便测试
        print("{}使用{}对{}造成{}伤害".format(damage.atker.name, damage.name, damage.defer.name, damage.val))
        # 受攻击后的被动触发判定
        if damage.trigger:
            for each in self.trigger_by_hit:
                each.action(damage)
    
    def damage_apply(self, damage):
        if damage.val > self.status.shield:
            self.status.shield = 0
            self.status.hp -= damage.val - self.status.shield
        else:
            self.status.shield -= damage.val

# 第一个实验性的式神，大天狗
class BigDog(Servant):
    "大天狗"
    def config(self):
        super().config(servant_base.BigDog)

    def set_skills(self):
        self.skill_1 = skill_.BigDogSKill1(self)
        self.skill_3 = skill_.BigDogSKill3(self)

class Bird(Servant):
    "姑获鸟"
    def config(self):
        super().config(servant_base.Bird)
    
    def set_skills(self):
        self.skill_1 = skill_.BirdSkill1(self)
        self.skill_3 = skill_.BirdSkill3(self)

class WineKing(Servant):
    "酒吞"
    def config(self):
        self.wine = 0
        super().config(servant_base.WineKing)

    
    def ai_act(self):
        targets = self.enemy.alive_members()
        if targets:
            target = max(targets, key=lambda x:x.status.get_hp_percent())
            self.skill_1(target)
    
    def set_skills(self):
        self.skill_1 = skill_.WineKingSkill1(self)
    
    def assist(self, target):
        temp = self.wine
        self.wine = 0
        super().assist(target)
        self.wine = temp

class LuSheng(Servant):
    "陆生"
    def config(self):
        super().config(servant_base.LuSheng)
    
    def set_skills(self):
        self.skill_1 = skill_.LuShengSkill1(self)
        self.skill_3 = skill_.LuShengSkill3(self)