"技能相关模块"
from damage_ import NormalDamage
from buff_ import Fear
from random import randint, choice

#技能基类
class baseSKill:
    "技能的抽象基类"
    def __init__(self, owner):
        self.owner = owner
        self.skill_id = 0
        self.config()
    
    def config(self):
        self.name = "普通攻击"
        self.cost = 0
        self.factor = 1
        self.showtime = 2
    
    def __call__(self, target):
        "技能释放过程"
        # 扣鬼火
        self.owner.team.energe_change(-self.cost)
        # 技能的实际过程
        self.action(target)
        # 记录本次输出
        self.owner.recorder.add_showtime(time=self.showtime)
        self.owner.recorder.add_skill(self.name)
    
    def action(self, target):
        "技能的过程，由子类重载"
        self.atk_one(target, self.factor)
    
    def atk_all(self, factor):
        for each in self.owner.enemy.alive_members():
            self.atk_one(each, factor)
    
    def atk_one(self, target, factor):
        dm = NormalDamage(self.owner)
        dm.name = self.name
        dm.factor = factor
        dm.skill_id = self.skill_id
        dm.set_defender(target)
        dm.run()

class ServantSkill1(baseSKill):
    "式神模版的一技能"
    pass

class ServantSkill3(baseSKill):
    "式神模版的三技能"
    def config(self):
        self.name = "暴跳如雷"
        self.cost = 3
        self.factor = 3
        self.showtime = 3
        self.skill_id = 3

class BigDogSKill1(baseSKill):
    "大狗一技能"
    def config(self):
        self.name = "风袭"
        self.cost = 0
        self.factor = 1.2
        self.showtime = 1

class BigDogSKill3(baseSKill):
    "大狗三技能"
    def config(self):
        self.name = "羽刃暴风"
        self.cost = 3
        self.showtime = 2.6
        self.skill_id = 3
    
    def action(self, target):
        for _ in range(4):
            self.atk_all(0.37 * 1.2)

class BirdSkill1(baseSKill):
    "姑获鸟的一技能"
    def config(self):
        self.name = "伞剑"
        self.cost = 0
        self.showtime = 1.1
        self.factor = 0.8 * 1.2
    
    def action(self, target):
        dm = NormalDamage(self.owner)
        dm.name = self.name
        dm.factor = self.factor
        dm.data_dict["def_reduce"] = 0.8
        dm.set_defender(target)
        dm.run()

class BirdSkill3(baseSKill):
    "姑获鸟的三技能"
    def config(self):
        self.name = "天翔鹤斩"
        self.cost = 3
        self.showtime = 2.15
        self.skill_id = 3
    
    def action(self, target):
        for _ in range(3):
            self.atk_all(0.33 * 1.24)
        self.atk_one(target, 0.88 * 1.24)

class WineKingSkill1(baseSKill):
    "酒吞1技能"
    def config(self):
        self.name = "酒葫芦"
        self.cost = 0
        self.showtime = 1.2 + (self.owner.wine * 0.5)
    
    def action(self, target):
        self.showtime = 1.2 + (self.owner.wine * 0.5)
        self.atk_one(target, 1.25)
        self.skill_id = 0
        for _ in range(self.owner.wine):
            self.atk_one(target, 1.25)
        self.skill_id = 1

class LuShengSkill1(baseSKill):
    "陆生1技能"
    def config(self):
        self.name = "弥弥切丸"
        self.cost = 0
        self.showtime = 1.5
        self.factor = 0.8 * 1.15
    
    def action(self, target):
        if randint(1, 1000) <= 250:
            assist_members = self.owner.team.alive_members()
            assist_members.remove(self.owner)
            for _ in range(randint(1,2)):
                if assist_members:
                    member = choice(assist_members)
                    assist_members.remove(member)
                    member.assist(target)
        
        super().action(target)

class LuShengSkill3(baseSKill):
    "陆生3技能"
    def config(self):
        self.name = "百鬼夜行"
        self.cost = 3
        self.showtime = 1.5
        self.factor = 1.2 * 1.2

    def action(self, target):
        Fear(self.owner).add(self.owner)
        super().action(target)


class YuZaoQianSkill1(baseSKill):
    "玉藻前1技能"
    def config(self):
        self.name = "灵击"
        self.cost = 0
        self.factor = 1.25
        self.showtime = 1.3
    
class YuZaoQianSkill2(baseSKill):
    "玉藻前2技能"
    def config(self):
        self.name = "狐火"
        self.cost = 3
        self.factor = 2.63 * 1.1
        self.showtime = 1.9
        self.combo = True
    
    def action(self, target):
        marker = target.status.get_hp_percent()
        if marker > 0.8:
            factor = self.factor * 0.85
        elif marker < 0.5:
            factor = self.factor * 1.15
        else:
            factor = self.factor
        self.atk_one(target, factor)
        if self.combo and not target.is_alive():
            self.owner.skill_3_combo(target)

class YuZaoQianSkill2Combo(YuZaoQianSkill2):
    "玉藻前连击时的二技能"
    def config(self):
        super().config()
        self.cost = 0
        self.showtime = 1.3
        self.combo = False
    
    def action(self, target):
        target = min(target.team.alive_members(), key=lambda x: x.status.get_hp_precent())
        super().action(target)

class YuZaoQianSkill3(baseSKill):
    "玉藻前三技能"
    def config(self):
        self.cost = 3
        self.name = "堕天"
        self.factor = 1.31 * 1.1
        self.showtime = 2.05
        self.combo = True
    
    def action(self, target):
        targets = target.team.alive_members()
        for each in targets:
            self.atk_one(each, self.factor)
        if self.combo and any(not x.is_alive for x in targets):
            self.owner.skill_2_combo(target)
    
    def atk_one(self, target, factor):
        marker = target.status.get_hp_percent()
        if marker > 0.8:
            factor = factor * 1.15
        elif marker < 0.5:
            factor = factor * 0.85
        super().atk_one(target, factor)

class YuZaoQianSkill3Combo(YuZaoQianSkill3):
    "玉藻前连击用三技能"
    def config(self):
        super().config()
        self.combo = False

