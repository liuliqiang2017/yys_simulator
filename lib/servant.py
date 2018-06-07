"""
式神相关类， 包括式神数据类Servant_Data, 伤害统计类Statistic， 式神基类
"""
from collections import defaultdict
from random import choice

from . import servant_base_data
from . import skill_

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
        # 导入御魂信息
        for yh in data_dict["yuhun"]:
            yh(self.owner).add(self.owner)

    def set_base_data(self):
        "导入式神的基础属性"
        base_data = getattr(servant_base_data, self.owner.__class__.__name__)
        self.base_atk = base_data["base_atk"]
        self.base_def = base_data["base_def"]
        self.base_speed = base_data["base_speed"]
        self.base_cri = base_data["base_cri"]
        self.base_criDM = base_data["base_criDM"]
        self.base_max_hp = base_data["base_max_hp"]
        # 导入被动技能
        for passive_skill in base_data["passive"]:
            passive_skill(self.owner).add(self.owner)
    
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

    def change_harm_ratio(self, ratio_num):
        "改变承伤比率"
        self.harm_ratio += ratio_num
    
    def change_atk_ratio(self, ratio_num):
        "改变基础攻击力"
        self.atk_ratio += ratio_num
    
    def change_def_ratio(self, ratio_num):
        "改变基础防御力"
        self.def_ratio += ratio_num
    
    def change_extra_criDM(self, num):
        "改变额外暴伤"
        self.extra_criDM += num

# 式神被动御魂管理类
class PassiveManage:
    "被动，御魂等管理类"
    def __init__(self):
        super().__init__()
        self.pre_round = []
        self.post_round = []
        self.pre_skill = []
        self.pre_hit = []
        self.post_hit = []
        self.post_skill = []
        self.be_hit = []

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

    def action_pre_hit(self, target):
        self.stimulate(target, self.pre_hit)

    def action_post_hit(self, target):
        self.stimulate(target, self.post_hit)
    
    def action_post_skill(self, target):
        self.stimulate(target, self.post_skill)

    def action_be_hit(self, target):
        self.stimulate(target, self.be_hit)

class ServantPassive(PassiveManage):
    "式神被动"
    
    def add_passive(self, passive):
        self.add(passive)
    
    def remove_passive(self, passive):
        self.remove(passive)
    
    def has_passive(self, passive):
        return bool([item for item in self.__dict__[passive.position] if isinstance(item, type(passive))])

class ServantYuHun(PassiveManage):
    "式神御魂"
    def add_yuhun(self, yuhun):
        self.add(yuhun)
    
    def remove_yuhun(self, yuhun):
        self.remove(yuhun)
    
    def has_yuhun(self, yuhun):
        return bool([item for item in self.__dict__[yuhun.position] if isinstance(item, type(yuhun))])

class ServantHelper(PassiveManage):
    "式神的其他触发，比如记仇，土蜘蛛等"
    
    def add_helper(self, helper):
        self.add(helper)
    
    def remove_helper(self, helper):
        self.remove(helper)
    
    def remove_same_helper(self, helper):
        self.get_same_helper(helper)[0].remove()
    
    def get_same_helper(self, helper):
        return [item for item in self.__dict__[helper.position] if isinstance(item, type(helper))]
    
    def has_helper(self, helper):
        return bool([item for item in self.__dict__[helper.position] if isinstance(item, type(helper))])

    def get_same_owner_helper(self, helper):
        return [item for item in self.__dict__[helper.position] if isinstance(item, type(helper)) and item.owner is helper.owner]

class BuffManage:
    "状态管理类"
    def __init__(self):
        super().__init__()
        self.buffs = []
    
    def has_buff(self, buff_cls):
        return bool([buff for buff in self.buffs if isinstance(buff, buff_cls)])

    def get_same_buff(self, other_buff):
        return [buff for buff in self.buffs if isinstance(buff, type(other_buff))]
    
    def get_same_caster_buff(self, other_buff):
        return [buff for buff in self.buffs if isinstance(buff, type(other_buff)) and buff.caster == other_buff.caster]
    
    def add_buff(self, buff):
        self.buffs.append(buff)
    
    def remove_buff(self, buff):
        self.buffs.remove(buff)
    
    def update_buffs(self):
        for buff in self.buffs:
            buff.update_layer()
    
    def remove_same_buff(self, buff):
        self.get_same_buff(buff)[0].remove()

class Statistic:

    "伤害统计类"
    def __init__(self, owner):
        self.owner = owner
        self.record = dict(
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
        self.record["name"] = self.owner.name
        return self.record   


class baseServant:
    "式神类基类"
    
    def __init__(self):
        super().__init__()
        self.name = ""
        self.status = ServantData(self)
        self.recorder = Statistic(self)
        self.yuhun = ServantYuHun()
        self.passive = ServantPassive()
        self.helper = ServantHelper()
        self.buffs = BuffManage()
        self.location = 0
        self.immune = False
        self.team = None
        self.enemy = None
        self.config()
        self.set_skills()

    def __getattr__(self, attr):
        "委托模式，把一些方法委托给子组件完成"
        delegate_route = ("status", "recorder", "yuhun", "passive", "helper", "buffs")
        for position in delegate_route:
            try:
                return getattr(super().__getattribute__(position), attr)
            except AttributeError:
                continue
        raise AttributeError("'{}' object has no attribute '{}'".format(self.__class__.__name__, attr))
    
    def set_skills(self):
        raise NotImplementedError
    
    def config(self):
        raise NotImplementedError

    def is_alive(self):
        return self.status.hp > 0
    
    def move(self, distance=None):
        self.location += distance if distance else self.status.get_speed()

class Servant(baseServant):
    "式神类"
    def __init__(self, data_dict):
        super().__init__()
        self.data_dict = data_dict
        self.classify = "式神"
    
    def initialize_servant(self):
        self.name = self.data_dict.get("name", "未命名")
        self.status.set_servant_status(self.data_dict)
        self.status.set_base_data()
        self.location = self.status.get_speed()
    
    def config(self):
        pass
    
    def set_skills(self):
        self.skill_1 = skill_.ServantSkill1(self)
        self.skill_3 = skill_.ServantSkill3(self)

    def trigger(self, target, *, flag):
        getattr(self.passive, flag)(target)
        getattr(self.yuhun, flag)(target)
        getattr(self.helper, flag)(target)
    
    def trigger_for_damage(self, target, checker, *, flag):
        condition = checker.get_trigger()
        if condition[0]:
            getattr(self.yuhun, flag)(target)
        if condition[1]:
            getattr(self.passive, flag)(target)
        if condition[2]:
            getattr(self.helper, flag)(target)
    
    def ai_act(self):
        "自动战斗时的ai，此处是最基础的3火开大ai"
        target = self.enemy.best_choice()
        if target:                
            if self.team.energe >= self.skill_3.cost:
                self.skill_3(target)
            else:
                self.skill_1(target)
    
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
        real_damage = self.damage_apply(damage)
        damage.set_damage_result(real_damage)
        # 受攻击后的被动触发判定
        self.trigger_for_damage(damage, damage.get_def_trigger(), flag="action_be_hit")
    
    def damage_apply(self, damage):
        real_damage = damage.val - self.status.shield
        if real_damage > 0:
            self.status.shield = 0            
            self.status.hp_change(-real_damage)
            return real_damage 
        self.status.shield += real_damage
        return 0


# 以下是一些式神
class BigDog(Servant):
    "大天狗"

    def set_skills(self):
        self.skill_1 = skill_.BigDogSKill1(self)
        self.skill_3 = skill_.BigDogSKill3(self)

class Bird(Servant):
    "姑获鸟"
    
    def set_skills(self):
        self.skill_1 = skill_.BirdSkill1(self)
        self.skill_3 = skill_.BirdSkill3(self)

class WineKing(Servant):
    "酒吞"
    def config(self):
        self.wine = 0
    
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
    
    def set_skills(self):
        self.skill_1 = skill_.LuShengSkill1(self)
        self.skill_3 = skill_.LuShengSkill3(self)

class YuZaoQian(Servant):
    "玉藻前"
    def config(self):
        self.status.def_break = 100

    def ai_act(self):
        targets = self.enemy.alive_members()
        if targets:                
            if self.team.energe >= self.skill_3.cost:
                if len(targets) > 1:
                    self.skill_3(choice(targets))
                else:
                    self.skill_2(targets[0])
            else:
                self.skill_1(choice(targets))
    
    def set_skills(self):
        self.skill_1 = skill_.YuZaoQianSkill1(self)
        self.skill_2 = skill_.YuZaoQianSkill2(self)
        self.skill_3 = skill_.YuZaoQianSkill3(self)
        self.skill_2_combo = skill_.YuZaoQianSkill2Combo(self)
        self.skill_3_combo = skill_.YuZaoQianSkill3Combo(self)

class ShuWeng(Servant):
    "书翁"
    
    def set_skills(self):
        self.skill_1 = skill_.ShuWengSkill1(self)
        self.skill_3 = skill_.ShuWengSkill3(self)

class UglyGirl(Servant):
    "丑女"

    def set_skills(self):
        self.skill_1 = skill_.UglyGirlSkill1(self)
        self.skill_3 = skill_.UglyGirlSkill3(self)
    
    def ai_act(self):
        if self.enemy.pet:
            self.skill_1(self.enemy.best_choice())
        else:
            super().ai_act()
    
class Peach(Servant):
    "桃子"
    
    def set_skills(self):
        self.skill_1 = skill_.PeachSkill1(self)
        self.skill_3 = skill_.PeachSkill3(self)

class QingMing(Servant):
    "晴明"
    def __init__(self):
        data = {"hp":27140, "atk":6382, "cri":0, "criDM":150, "speed":128, "def_":1051, "yuhun":[], "name": "晴明"}
        super().__init__(data)
    
    def set_skills(self):
        self.skill_1 = skill_.QingMingSkill1(self)
        self.skill_2 = skill_.QingMingSkill2(self)
        self.skill_3 = skill_.QingMingSkill3(self)

    
    def ai_act(self):
        from . buff_ import Xing
        if self.has_buff(Xing):
            self.skill_2(self)
        else:
            self.skill_3(self)

# 召唤物等
class basePet(Servant):
    "宠物类基类"

    def create(self):
        raise NotImplementedError

    def remove(self):
        raise NotImplementedError

class Scarecrow(basePet):
    "丑女的草人"
    def __init__(self, owner, target):
        self.owner = owner
        self.target = target
        data_dict = self.make_data_dict(target)
        super().__init__(data_dict)
        self.initialize_servant()
        self.round_num = 2
        self.location = 0
    
    def make_data_dict(self, target):
        data_dict = dict(atk=0, yuhun=[], cri=0, criDM=0)
        data_dict["name"] = "草人"
        data_dict["hp"] = target.status.get_max_hp() * 0.3
        data_dict["speed"] = target.status.get_speed()
        data_dict["def_"] = target.status.def_ * 0.5
        return data_dict
    
    def config(self):
        self.classify = "召唤物"
        self.create()
    
    def ai_act(self):
        "草人什么也不干"
        pass
    
    def create(self):
        self.target.team.add_pet(self)
    
    def remove(self):
        self.target.team.remove_pet(self)
        self.status.hp = -1