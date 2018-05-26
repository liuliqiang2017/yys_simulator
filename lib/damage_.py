"伤害类，负责实现伤害的结算"
from random import randint

class Damage:
    "伤害基类"
    def __init__(self, atk_dict):
        super().__init__()
        self.data_dict = atk_dict
        self.atker = atk_dict["atker"]
        self.name = atk_dict["name"]
        self.config()
        self.counter = True
        self.trigger = True
        self.critical = False
    
    def config(self):
        pass
    
    def set_defender(self, defender):
        self.defer = defender
        self.data_dict.update(defender.get_def_data())
    
    def calculate(self, data_dict):
        "计算伤害值，由子类实现不同的计算方法"
        raise NotImplementedError
    
    def get_result(self):
        self.val = self.calculate(self.data_dict)
        return self

    def _cri_check(self):
        if randint(1, 1000) <= self.data_dict["cri"] * 10:
            self.critical = True
        return self.critical

class NormalDamage(Damage):
    "正常伤害，计算防，触发被动等"
    
    def calculate(self, data_dict):
        criDM = data_dict["criDM"] if self._cri_check() else 100
        atk_dm = data_dict["atk"] * criDM * 3 * data_dict["factor"] * data_dict["damage_ratio"] * data_dict["harm_ratio"]
        def_dm = (data_dict["def"] + data_dict["extra_def"] - data_dict["def_break"]) * data_dict["def_reduce"] + 300
        dm = atk_dm / def_dm
        return round(dm)

class Counter_Damage(NormalDamage):
    "反击伤害，正常伤害的一种，不可被反击"
    def config(self):
        self.counter = False

# TODO 伤害结算方式
class IndirectDamage(Damage):
    "间接伤害，计算防，不触发被动"
    def config(self):
        self.name = "间接伤害"
        self.counter = False
        self.trigger = False

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