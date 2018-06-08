"伤害类，负责实现伤害的结算"
from random import randint

# 触发管理类
class baseTrigger:
    "触发基类"
    def __init__(self):
        super().__init__()
        self.yuhun = True
        self.passive = True
        self.helper = True
        self.specific = [] # 特殊的规则放在这里
    
    def set_trigger(self, y, p, h):
        self.yuhun = bool(y)
        self.passive = bool(p)
        self.helper = bool(h)
    
    def merge_trigger(self, y, p, h):
        self.yuhun = self.yuhun and bool(y)
        self.passive = self.passive and bool(p)
        self.helper = self.helper and bool(h)
    
    def get_trigger(self):
        return self.yuhun, self.passive, self.helper
    
    def add_specific(self, spe):
        self.specific.append(spe)
    
    def get_specific(self):
        return self.specific

    def remove_specific(self, spe):
        self.specific.remove(spe)

class AttackTrigger(baseTrigger):
    "攻击方触发器"
    pass

class DefenderTrigger(baseTrigger):
    "防守方触发器"
    pass

class Damage:
    "伤害基类"
    def __init__(self, atker):
        super().__init__()
        self.data_dict = atker.get_atk_data()
        self.atker = atker
        self.name = "默认攻击"
        self.factor = 1
        self.skill_id = 0 # 由哪个位置技能发动，以此判断是否能协战
        self.atk_trigger = AttackTrigger()
        self.def_trigger = DefenderTrigger()
        # self.took_effect = []
        self.critical = False # 是否暴击
        self.config()
    
    def config(self):
        pass
    
    def set_damage_result(self, val):
        self.result = val
    
    def set_skill(self, skill):
        self.skill = skill
        self.factor = getattr(skill, "factor", 1)
        self.skill_id = skill.skill_id
        self.atker = skill.owner
        self.atk_trigger.merge_trigger(*skill.get_atk_trigger())
        self.def_trigger.merge_trigger(*skill.get_def_trigger())
    
    def get_damage_result(self):
        return self.result

    def set_defender(self, defender):
        self.defer = defender
        self.data_dict.update(defender.status.get_def_data())
    
    def calculate(self, data_dict):
        "计算伤害值，由子类实现不同的计算方法"
        raise NotImplementedError
    
    def get_def_trigger(self):
        return self.def_trigger
    
    # def add_effect(self, actor):
    #     self.took_effect.append(actor)
    
    # def has_effect(self, actor):
    #     return bool([effect for effect in self.took_effect if isinstance(effect, type(actor))])
    
    def run(self):
        # 触发攻击前生效的御魂和被动
        self.atker.trigger_for_damage(self, self.atk_trigger, flag="action_pre_hit")
        # 计算伤害
        self.val = self.calculate(self.data_dict)
        # 触发攻击后生效的御魂和被动, 触发specific里的御魂
        self.atker.trigger_for_damage(self, self.atk_trigger, flag="action_post_hit")
        for each in self.atk_trigger.get_specific():
            if not getattr(self.atker, "has_" + each.classify)(each):
                each.action(self)
        # 生效伤害,记录本次的值
        self.defer.defend(self)
        # 传递给攻击者的记录器
        self.atker.recorder_add_damage(self)
        # 如果有skill，回传skill伤害值
        if hasattr(self, "skill"):
            self.skill.add_skill_result(self.defer, self.result)


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
        return dm

class Counter_Damage(NormalDamage):
    "反击伤害，正常伤害的一种，不可被反击"
    def config(self):
        self.counter = False

# TODO 伤害结算方式
class IndirectDamage(Damage):
    "间接伤害，计算防，不触发双方御魂，触发被动"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
    def config(self):
        self.name = "间接伤害"
        self.atk_trigger.set_trigger(False, True, True)
        self.def_trigger.set_trigger(False, True, True)


class NoteDamage(IndirectDamage):
    "书翁的记仇结算"

    def set_base_val(self, val):
        self.base_val = val
    
    def calculate(self, data_dict):
        criDM = data_dict["criDM"] if self._cri_check() else 100
        atk_dm = self.base_val * criDM * data_dict["damage_ratio"] * data_dict["harm_ratio"] * 3 
        def_dm = (data_dict["def"] + data_dict["extra_def"] - data_dict["def_break"]) * data_dict["def_reduce"] + 300
        dm = round(atk_dm / def_dm)
        max_dm = self.atker.status.get_max_hp() * 12
        return min(dm, max_dm)

class RealDamage(Damage):
    "真实伤害，不计算防，触发被动"


    def config(self):
        self.name = "真实伤害"    

    def set_base_val(self, val):
        self.base_val = val
    
    def calculate(self, data_dict):
        return self.base_val


class NeedleDamage(RealDamage):
    "针女伤害，真实伤害的一种"
    def config(self):
        super().config()
        self.name = "针女"

    def calculate(self, data_dict):
        dm = min(data_dict["atk"] * 1.2, data_dict["max_hp"] * 0.1)
        return round(dm)

class AbsDamage(RealDamage):
    "绝对伤害，什么不触发，什么都不吃"
    def config(self):
        super().config()
        self.atk_trigger.set_trigger(False, False, False)
        self.def_trigger.set_trigger(False, False, False)
