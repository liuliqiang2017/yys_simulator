"""
被动技能以及御魂类
act_period：触发时间，数值分为1X,2X, 3X，4X 方便扩展分别如下
1x：从11到19，为回合开始前的时段
    11. 回合开始前触发，比如大天狗的加攻击，作用于owner
2x：从21到29，为回合中的时段
    21. 攻击前触发，比如网切等，作用于damage, 无论有没有伤害
    23. 攻击后有伤害触发(相当于攻击后)， 破势，针女，各种控制御魂，作用于damage
3x：从31到39，为回合结束的时段
    31. 回合结束时触发，比如招财猫，轮入道等，作用于owner
4x：从41到49，为回合外的时段
    41. 受到攻击后触发（有伤害），金刚经，返魂香，铮，还有一些反击等。
如果多个时间段触发，如酒吞被打和回合结束，那就写两个被动。
注：觉醒带来的效果直接写入基础属性里，不单独作为被动技能实现。有些被动完全和技能挂钩的直接写在技能里，也不单独实现
action: 触发过程
"""
from random import randint
import buff_
import damage_


class basePassive:
    "被动效果基类"
    def __init__(self, owner):
        super().__init__()
        self.owner = owner
        self.config()
    
    def config(self):
        self.act_period = 0
    
    def add(self, target):
        self.owner = target
        if self.act_period == 11:
            self.owner.trigger_pre_round.append(self)
        elif self.act_period == 21:
            self.owner.trigger_pre_skill.append(self)
        elif self.act_period == 23:
            self.owner.trigger_post_skill.append(self)
        elif self.act_period == 31:
            self.owner.trigger_post_round.append(self)
        elif self.act_period == 41:
            self.owner.trigger_by_hit.append(self)
        
    
    def action(self):
        "触发效果，由子类实现"
        raise NotImplementedError

class PassiveSkill(basePassive):
    "被动技能类"
    pass

class YuHun(basePassive):
    "御魂类"
    pass

# TODO 被动技能：鸟的协战，荒的开幻境

class SteelFeather(PassiveSkill):
    "天狗的铁毛，目前只有伤害加成部分"
    def config(self):
        self.act_period = 11
    
    def action(self):
        "给owner加个buff"
        buff_.SteelMao(self.owner).add(self.owner)

class Curse(PassiveSkill):
    "丑女的诅咒"
    def config(self):
        self.act_period = 33
    
    def action(self):
        "给对面随机人员上个buff"
        target = self.owner.enemy.random_member()
        buff_.CurseFire(self.owner).add(target)

class DrinkPostRound(PassiveSkill):
    "酒吞回合结束喝酒"
    def config(self):
        self.act_period = 31
    
    def action(self):
        "本大爷要喝一口酒"
        if self.owner.wine < 4 and randint(1, 1000) <= 500:
            self.owner.wine += 1

class DrinkByHit(PassiveSkill):
    "酒吞被打喝酒"
    def config(self):
        self.act_period = 41
    
    def action(self, damage):
        if self.owner.wine < 4 and randint(1, 1000) <= 250:
            self.owner.wine += 1

# TODO 御魂：土蜘蛛。

class Needle(YuHun):
    "针女"
    def config(self):
        self.act_period = 23
    
    def action(self, damage):
        "破盾暴击有40%几率，由damage的攻击方向防守方造成一次真实伤害"
        if  damage.critical and damage.val > damage.defer.status.shield and randint(1, 1000) <= 400:
            needle_dm = damage_.NeedleDamage(damage.atker)
            needle_dm.set_defender(damage.defer)
            needle_dm.run()

class NetCut(YuHun):
    "网切"
    def config(self):
        self.act_period = 21
    
    def action(self, damage):
        "50%几率降低对方45%的防御"
        if randint(1, 1000) <= 500:
            damage.data_dict["def_reduce"] *= 0.55

class BadThing(YuHun):
    "破势"
    def config(self):
        self.act_period = 23
    
    def action(self, damage):
        "对方血量超过70%，伤害增加40%"
        if damage.defer.status.hp / damage.defer.status.max_hp >= 0.7:
            damage.val *= 1.4

class LuckyCat(YuHun):
    "招财猫"
    def config(self):
        self.act_period = 11
    
    def action(self):
        "回合开始概率回2火"
        if randint(1, 1000) <= 500:
            self.owner.team.energe_change(2)