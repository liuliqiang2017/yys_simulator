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

