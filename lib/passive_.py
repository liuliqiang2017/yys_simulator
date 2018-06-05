"""
被动技能以及御魂类
由属性position决定触发时间分别如下
"pre_round" : 回合前
"pre_skill" : 技能命中前
"post_skill" : 技能命中后
"post_round" :回合后
"by_hit" : 被攻击时

初始化时需要传入实例的创建者owner， 将实例添加到目标时需要调用add(target)， 删除remove()， 生效action(target)接收一个目标参数
如果多个时间段触发，如酒吞被打和回合结束，那就写两个被动。
注：觉醒带来的效果直接写入基础属性里，不单独作为被动技能实现。有些被动完全和技能挂钩的直接写在技能里，也不单独实现
action: 触发过程
"""
from functools import wraps
from random import randint
from . import buff_
from . import damage_

# 一个单例装饰器
def sington(cls):
    "单例模式"
    if "_instance" not in cls.__dict__:
        cls._instance = None
    @wraps(cls)
    def wrapper(*args, **kwargs):
        if cls._instance is None:
            cls._instance = cls(*args, **kwargs)    
        return cls._instance
    return wrapper


class basePassive:
    "被动效果基类"
    def __init__(self, owner=None):
        super().__init__()
        self.owner = owner
        self.position = ""
        self.config()
    
    def config(self):
        "做一些配置，由子类实现"
        raise NotImplementedError
    
    def add(self, target):
        raise NotImplementedError

    
    def remove(self):
        raise NotImplementedError
    
    def action(self):
        "触发效果，由子类实现"
        raise NotImplementedError

class PassiveSkill(basePassive):
    "被动技能类"
    def __init__(self, owner=None):
        super().__init__(owner)
        self.classify = "passive"
    
    def add(self, target):
        self.target = target
        target.add_passive(self)
    
    def remove(self):
        self.target.remove_passive(self)

class YuHun(basePassive):
    "御魂类"
    def __init__(self, owner=None):
        super().__init__(owner)
        self.classify = "yuhun"
    
    def add(self, target):
        self.target = target
        target.add_yuhun(self)

    def remove(self):
        self.target.remove_yuhun(self)


class SteelFeather(PassiveSkill):
    "天狗的铁毛，目前只有伤害加成部分"
    def config(self):
        self.position = "pre_round"
    
    def action(self, target):
        "给owner加个buff"
        buff_.SteelMao(self.owner).add(target)

class Curse(PassiveSkill):
    "丑女的诅咒"
    def config(self):
        self.position = "post_round"
    
    def action(self, target):
        "给对面随机人员上个buff"
        aim = target.enemy.random_member()
        if aim:
            buff_.CurseFire(self.owner).add(aim)

class DrinkPostRound(PassiveSkill):
    "酒吞回合结束喝酒"
    def config(self):
        self.position = "post_round"
    
    def action(self, target):
        "本大爷要喝一口酒"
        if target.wine < 4 and randint(1, 1000) <= 500:
            target.wine += 1

class DrinkByHit(PassiveSkill):
    "酒吞被打喝酒"
    def config(self):
        self.position = "by_hit"
    
    def action(self, damage):
        if damage.defer.wine < 4 and randint(1, 1000) <= 250:
            damage.defer.wine += 1

# TODO 御魂：土蜘蛛。

@sington
class NoneYuHun(YuHun):
    "空御魂，无效果"
    def config(self):
        pass

    def add(self, target):
        pass

@sington
class Needle(YuHun):
    "针女"
    def config(self):
        self.position = "post_skill"
    
    def action(self, damage):
        "破盾暴击有40%几率，由damage的攻击方向防守方造成一次真实伤害"
        if  damage.critical and damage.val > damage.defer.status.shield and randint(1, 1000) <= 400:
            needle_dm = damage_.NeedleDamage(damage.atker)
            needle_dm.set_defender(damage.defer)
            needle_dm.run()
@sington
class NetCut(YuHun):
    "网切"
    def config(self):
        self.position = "pre_skill"
    
    def action(self, damage):
        "50%几率降低对方45%的防御"
        if randint(1, 1000) <= 500:
            damage.data_dict["def_reduce"] *= 0.55
@sington
class BadThing(YuHun):
    "破势"
    def config(self):
        self.position = "post_skill"
    
    def action(self, damage):
        "对方血量超过70%，伤害增加40%"
        if damage.defer.status.get_hp_percent() >= 0.7:
            damage.val *= 1.4
@sington
class HeartEye(YuHun):
    "心眼"
    def config(self):
        self.position = "post_skill"

    def action(self, damage):
        "对方血量低于30%， 伤害增加50%"
        if damage.defer.status.get_hp_percent() <= 0.3:
            damage.val *= 1.5

class LuckyCat(YuHun):
    "招财猫"
    def config(self):
        self.position = "pre_round"
    
    def action(self, target):
        "回合开始概率回2火"
        if randint(1, 1000) <= 500:
            target.team.energe_change(2)

class DustSpider(YuHun):
    "土蜘蛛"
    def config(self):
        self.position = "post_skill"
    
    def action(self, damage):
        "给对方上个helper,回合后触发"
        helper = DustSpiderRecorder(self.owner)
        helper.val = damage.val * 0.25
        helper.add(damage.defer)



# 以下是helper的一些东西

class Linker(basePassive):
    "联动器基类"
    def __init__(self, owner):
        self._link = []
        self.classify = "helper"
        self.coexist_num = 1000
        super().__init__(owner)

    def add(self, target):
        self.target = target
        same = target.get_same_helper(self)
        if len(same) < self.coexist_num:
            target.add_helper(self)
    
    def remove(self):
        self.target.remove_helper(self)

    
    def link_to(self, link):
        link._link.append(self)
    
    def link_cut(self, link):
        if self in link._link:
            link._link.remove(self)


class AssistAtk(Linker):
    "协战, 把观察者放在每个其他友方式神的触发里"
    def config(self):
        self.chance = 300
        self.position = "pre_skill"
    
    def add(self, target):
        for each in target.team.members:
            if each is not self.owner:
                each.add_passive(self)

    def remove(self):
        for each in self.owner.team.members:
            if each is not self.owner:
                each.remove_passive(self)
    
    def action(self, damage):
        if all([self.owner.is_alive(),
               damage.skill_id == 1,
               randint(1, 1000) <= self.chance]):
            self.owner.assist(damage.defer)

# 荒的幻境协战
class HuangAssist(AssistAtk):
    "荒的协战"
    def config(self):
        super().config()
        self.chance = 500
    
    def action(self, damage):
        if self.owner.aura:
            super().action(damage)


# 鸟的协战
class BirdAssist(AssistAtk):
    "鸟的协战"
    pass

# 书翁记仇。
class TakeNotes(Linker):
    "书翁记仇的分体, 主体作为被动存在"
    def config(self):
        self.dm_memo = 0
        self.position = "by_hit"
        self.link_to(self.owner.notebook)
    
    def action(self, damage):
        self.dm_memo += damage.val
    
    def explode(self):
        dm = damage_.NoteDamage(self.owner)
        dm.name = "死亡笔记"
        dm.set_defender(self.target)
        dm.set_base_val(self.dm_memo)
        dm.run()
        self.remove()

class Notebook(Linker):
    "书翁记仇的主体"
    def config(self):
        self.position = "pre_round"

    def add(self, target):
        super().add(target)
        self.owner.notebook = self
    
    def action(self, target):
        for each in self._link[:]:
            if each.target.is_alive():
                each.explode()
            each.link_cut(self)

class Transit(Linker):
    "草人传递伤害"
    def config(self):
        self.position = "by_hit"
    
    def action(self, damage):
        dm = damage_.RealDamage(self.owner.owner)
        dm.name = "草人传递"
        dm.set_base_val(damage.val)
        dm.set_defender(self.owner.target)
        dm.run()
        # 传递完判定owner以及target是否死亡, 任意一方死亡则删除草人
        if not (self.owner.is_alive() and self.owner.target.is_alive()):
            self.owner.remove()

class CheakRound(Linker):
    "草人回合检测"
    def config(self):
        self.position = "post_round"
    
    def action(self, target):
        target.round_num -= 1
        if target.round_num <= 0:
            target.remove()

class DustSpiderRecorder(Linker):
    "土蜘蛛伤害记录器，回合后爆发"
    def config(self):
        self.val = 0
        self.coexist_num = 3
        self.position = "post_round"
    
    def action(self, target):
        damage = damage_.AbsDamage(self.owner)
        damage.set_base_val(self.val)
        damage.name = "土蜘蛛"
        damage.set_defender(self.target)
        damage.run()
        self.remove()