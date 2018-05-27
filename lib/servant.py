"""
式神相关类， 包括式神数据类Servant_Data, 式神技能类Servant_Skill, 伤害统计类Statistic， 式神基类
"""
from collections import defaultdict
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

    def get_max_hp(self):
        return self.max_hp + self.base_max_hp * self.max_hp_ratio

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
        self.name = data_dict.get("name", "式神")
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
        self.config()

    def config(self, base=servant_base.BOSS_DUMMY):
        "由子类实现不同的初始设置，以下是个例子"
        # 初始化式神的基础属性
        self.status.set_base_data(base)
        # 设置式神的御魂
        for yh in self.data_dict["yuhun"]:
            yh().add(self)
        # 设置式神的被动
        for passive_skill in base["passive"]:
            passive_skill().add(self)
        # 使用开场运行一次的技能
        for each in self.run_once:
            each.action()
    
    def is_alive(self):
        return self.status.hp > 0
    
    def move(self, distance=None):
        self.location += distance if distance else self.status.get_speed()

    def skill_1(self, target, cost=0):
        # 扣鬼火
        self.team.energe_change(-cost)
        # 输出伤害
        damage = NormalDamage(self)
        damage.name = "普通攻击"
        damage.factor = 1.25
        damage.set_defender(target)
        damage.run()
        # 记录输出,add_showtime的参数为动画时间
        self.recorder.add_showtime(time=1)
        self.recorder.add_skill(damage.name)
    
    def skill_2(self, targets, cost=0):
        # 这三个技能都需要子类去分别重载
        pass
    
    def skill_3(self, target, cost=3):
        self.team.energe_change(-cost)
        damage = NormalDamage(self)
        damage.name = "暴跳如雷"
        damage.factor = 3
        damage.set_defender(target)
        damage.run()
        # 记录输出,add_showtime的参数为动画时间
        self.recorder.add_showtime(time=3)
        self.recorder.add_skill(damage.name)
    
    def ai_act(self):
        "自动战斗时的ai，此处是最基础的3火开大ai"
        targets = self.enemy.alive_members()
        if targets:                
            if self.team.energe >= 3:
                self.skill_3(choice(targets))
            else:
                self.skill_1(choice(targets))
    
    def counter(self, target):
        "反击，默认用一技能反击"
        self.assist(target)
    
    def assist(self, target):
        "协战，默认用一技能协战"
        if target.is_alive():
            self.skill_1([target])
        else:
            self.skill_1(self.enemy.alive_members())
        
    def defend(self, damage):
        # 结算伤害
        self.damage_apply(damage)
        # 受攻击后的被动触发判定
        if damage.trigger:
            for each in self.trigger_by_hit:
                each.action(damage)
    
    def damage_apply(self, damage):
        self.status.hp -= damage.val
        print("{}对{}发动{}，造成{}伤害".format(damage.atker.name, damage.defer.name, damage.name, damage.val))
        print("{}的剩余血量是{}".format(self.name, self.status.hp))
    





