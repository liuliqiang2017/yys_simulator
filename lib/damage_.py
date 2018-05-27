"伤害类，负责实现伤害的结算"
from random import randint

class Damage:
    "伤害基类"
    def __init__(self, atker):
        super().__init__()
        self.data_dict = atker.status.get_atk_data()
        self.atker = atker
        self.name = "默认攻击"
        self.factor = 1
        self.skill_id = 1 # 由哪个位置技能发动，以此判断是否能协战
        self.passive = True # 是否触发自己被动
        self.counter = True # 能否被反击
        self.trigger = True # 能否触发对方被动御魂
        self.critical = False # 是否暴击
        self.config()
    
    def config(self):
        pass
    
    def set_defender(self, defender):
        self.defer = defender
        self.data_dict.update(defender.status.get_def_data())
    
    def calculate(self, data_dict):
        "计算伤害值，由子类实现不同的计算方法"
        raise NotImplementedError
    
    def run(self):
        # 触发攻击前生效的御魂和被动
        if self.passive:
            for each in self.atker.trigger_pre_skill:
                each.action(self)
        # 计算伤害
        self.val = self.calculate(self.data_dict)
        # 触发攻击后生效的御魂和被动
        if self.passive:
            for each in self.atker.trigger_post_skill:
                each.action(self)
        # 生效伤害
        self.defer.defend(self)
        # 传递给攻击者的记录器
        self.atker.recorder.add_damage(self)

    def _cri_check(self):
        if randint(1, 1000) <= self.data_dict["cri"] * 10:
            self.critical = True
            return True
        return False

class NormalDamage(Damage):
    "正常伤害，计算防，触发被动等"
    
    def calculate(self, data_dict):
        criDM = data_dict["criDM"] if self._cri_check() else 100
        atk_dm = data_dict["atk"] * criDM * 3 * self.factor * data_dict["damage_ratio"] * data_dict["harm_ratio"]
        def_dm = (data_dict["def"] + data_dict["extra_def"] - data_dict["def_break"]) * data_dict["def_reduce"] + 300
        dm = atk_dm / def_dm
        return round(dm)

class Counter_Damage(NormalDamage):
    "反击伤害，正常伤害的一种，不可被反击"
    def config(self):
        self.counter = False

# TODO 伤害结算方式
class IndirectDamage(Damage):
    "间接伤害，计算防，不触发双方被动"
    def config(self):
        self.name = "间接伤害"
        self.passive = False
        self.trigger = False

class NoteDamage(IndirectDamage):
    "书翁的记仇结算"

    def set_base_val(self, val):
        self.base_val = val
    
    def calculate(self, data_dict):
        criDM = data_dict["criDM"] if self._cri_check() else 100
        atk_dm = self.base_val * criDM * 3
        def_dm = (data_dict["def"] + data_dict["extra_def"] - data_dict["def_break"]) * data_dict["def_reduce"] + 300
        dm = round(atk_dm / def_dm)
        max_dm = self.atker.status.get_max_hp() * 12
        return min(dm, max_dm)

class RealDamage(Damage):
    "真实伤害，不计算防，触发被动"
    pass

class NeedleDamage(RealDamage):
    "针女伤害，真实伤害的一种"
    def config(self):
        self.name = "针女"

    def calculate(self, data_dict):
        dm = min(data_dict["atk"] * 1.2, data_dict["max_hp"] * 0.1)
        return round(dm)