"技能相关模块"
from collections import defaultdict
from random import randint, choice

from .passive_ import TakeNotes
from .damage_ import NormalDamage, AttackTrigger, DefenderTrigger
from .buff_ import Fear, Mie, Xing, Doom


#技能基类
class baseSKill:
    "技能的抽象基类"
    def __init__(self, owner):
        self.owner = owner
        self.target = None
        self.kill = False
        self.skill_id = 0
        self.atk_trigger = AttackTrigger()
        self.def_trigger = DefenderTrigger()
        self.total_damage = defaultdict(float)
        self.config()
    
    def config(self):
        self.name = "普通攻击"
        self.cost = 0
        self.factor = 1
        self.showtime = 2
    
    def __call__(self, target):
        "技能释放过程"
        self.target = target
        # 扣鬼火
        self.owner.team.energe_change(-self.cost)
        # 触发技能前触发的效果
        self.owner.trigger(self, flag="action_pre_skill")
        # 技能的实际过程
        self.action(target)
        # 触发技能后触发的效果
        self.owner.trigger(self, flag="action_post_skill")
        # 记录本次输出,清空本次技能记录
        self.target = None
        self.total_damage.clear()
        self.record()
    
    def add_skill_result(self, key, val):
        self.total_damage[key] += val
    
    def get_skill_result(self):
        return self.total_damage
    
    def get_atk_trigger(self):
        return self.atk_trigger.get_trigger()
    
    def get_def_trigger(self):
        return self.def_trigger.get_trigger()
    
    def record(self):
        self.owner.recorder_add_showtime(time=self.showtime)
        self.owner.recorder_add_skill(self.name)
        self.owner.team.arena.add_showtime(time=self.showtime)

    def action(self, target):
        "技能的过程，由子类重载"
        self.atk_one(target, self.factor)
    
    def atk_all(self, factor):
        for each in self.owner.enemy.alive_members():
            self.atk_one(each, factor)
    
    def atk_one(self, target, factor):
        dm = NormalDamage(self.owner)
        dm.set_skill(self)
        dm.set_defender(target)
        dm.run()

class ServantSkill1(baseSKill):
    "式神模版的一技能"
    def __init__(self, owner):
        super().__init__(owner)
        self.skill_id = 1

class ServantSkill3(baseSKill):
    "式神模版的三技能"
    def __init__(self, owner):
        super().__init__(owner)
        self.skill_id = 3

class BigDogSKill1(ServantSkill1):
    "大狗一技能"
    def config(self):
        self.name = "风袭"
        self.cost = 0
        self.factor = 1.2
        self.showtime = 1

class BigDogSKill3(ServantSkill3):
    "大狗三技能"
    def config(self):
        self.name = "羽刃暴风"
        self.cost = 3
        self.showtime = 2.6
        self.skill_id = 3
    
    def action(self, target):
        for _ in range(4):
            self.atk_all(0.37 * 1.2)

class BirdSkill1(ServantSkill1):
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

class BirdSkill3(ServantSkill3):
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

class WineKingSkill1(ServantSkill1):
    "酒吞1技能"
    def config(self):
        self.name = "酒葫芦"
        self.cost = 0
        self.showtime = 1.2 + (self.owner.wine * 0.5)
    
    def action(self, target):
        self.showtime = 1.2 + (self.owner.wine * 0.5)
        self.atk_one(target, 1.25)
        for _ in range(self.owner.wine):
            self.atk_one(target, 1.25)

class HuaNiaoSkill1(ServantSkill1):
    "花鸟1技能"
    def config(self):
        self.name = "归鸟"
        self.cost = 0
        self.showtime = 1.5
    
    def action(self, target):
        self.atk_one(target, 0.4)
        for _ in range(self.owner.bird):
            self.atk_one(target, 0.4)

class LuShengSkill1(ServantSkill1):
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

class LuShengSkill3(ServantSkill3):
    "陆生3技能"
    def config(self):
        self.name = "百鬼夜行"
        self.cost = 3
        self.showtime = 1.5
        self.factor = 1.2 * 1.2

    def action(self, target):
        Fear(self.owner).add(self.owner)
        super().action(target)


class YuZaoQianSkill1(ServantSkill1):
    "玉藻前1技能"
    def config(self):
        self.name = "灵击"
        self.cost = 0
        self.factor = 1.25
        self.showtime = 1.3
    
class YuZaoQianSkill2(ServantSkill3):
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

class YuZaoQianSkill3(ServantSkill3):
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


class ShuWengSkill1(ServantSkill1):
    "书翁一技能"
    def config(self):
        self.name = "墨染"
        self.cost = 0
        self.factor = 1.25
        self.showtime = 1.2

class ShuWengSkill3(ServantSkill3):
    "书翁三技能"
    def config(self):
        self.name = "万象之书"
        self.cost = 2
        self.factor = 0.8
        self.showtime = 2.3
    
    def action(self, target):
        # 诅咒第一个目标
        self.note_one(target)
        # 第二个血少的目标
        others = target.team.alive_members()
        if target.is_alive():
            others.remove(target)
        if others:
            self.note_one(min(others, key=lambda x: x.status.get_hp_percent()))
    
    def note_one(self, target):
        note = TakeNotes(self.owner)
        note.add(target)
        self.atk_one(target, self.factor)

class UglyGirlSkill1(ServantSkill1):
    "丑女一技能"
    def config(self):
        self.name = "咒锥"
        self.cost = 0
        self.factor = 1.25
        self.showtime = 1.8

class UglyGirlSkill3(ServantSkill3):
    "丑女三技能"
    def config(self):
        self.name = "草人替身"
        self.cost = 2
        self.factor = 1
        self.showtime = 3
    
    def action(self, target):
        from .servant import Scarecrow
        if target.team.pet is None:
            pet = Scarecrow(self.owner, target)
            pet.config()


class PeachSkill1(ServantSkill1):
    "桃子一技能"
    def config(self):
        self.name = "兔狱卒·叱责"
        self.cost = 0
        self.factor = 1.25
        self.showtime = 1.5

class PeachSkill3(ServantSkill3):
    "桃子二技能"
    def config(self):
        self.name = "蜜桃·地狱偶像"
        self.cost = 2
        self.factor = 0
        self.showtime = 2.5
    
    def action(self, target):
        self.distance = self.owner.team.arena.run_bar * 0.25
        for each in self.owner.team.alive_members():
            self.pull_one(each)

    def pull_one(self, target):
        target.move(self.distance)
        target.status.hp_change(self.owner.status.get_max_hp() * 0.1)

class QingMingSkill1(ServantSkill1):
    "晴明普攻"
    def config(self):
        self.name = "基础术式"
        self.cost = 0
        self.factor = 1.2
        self.showtime = 1.25

class QingMingSkill2(ServantSkill3):
    "晴明灭"
    def config(self):
        self.name = "符咒·灭"
        self.cost = 0
        self.factor = 0
        self.showtime = 1.6
    
    def action(self, target):
        for each in target.enemy.alive_members():
            Mie(self.owner).add(each)

class QingMingSkill3(ServantSkill3):
    "晴明星"
    def config(self):
        self.name = "符咒·星"
        self.cost = 0
        self.factor = 0
        self.showtime = 1.8
    
    def action(self, target):
        for each in target.team.alive_members():
            Xing(self.owner).add(each)
    

class CiMuSkill1(ServantSkill1):
    "茨木1技能"
    def config(self):
        self.name = "黑焰"
        self.cost = 0
        self.factor = 1.25
        self.showtime = 1

class CiMuSkill3(ServantSkill3):
    "茨木3技能"
    def config(self):
        self.name = "地狱之手"
        self.cost = 3
        self.factor = 2.63 * 1.2
        self.showtime = 2.35
    
    def action(self, target):
        super().action(target)
        if not self.kill:
            Doom(self.owner).add(self.owner)
        else:
            for each in self.owner.get_same_buff(Doom(self.owner)):
                each.remove()

class HuangSkill1(ServantSkill1):
    "荒1技能"
    def config(self):
        self.name = "星轨"
        self.cost = 0
        self.factor = 1.25
        self.showtime = 1

class HuangSkill3(ServantSkill3):
    "荒3技能"
    def config(self):
        self.name = "天罚·星"
        self.cost = 3
        self.factor = 1.04
        self.showtime = 1
    
    def action(self, target):
        factor = self.factor
        for _ in range(self.cost):
            self.atk_one(target, factor)
            factor = factor * 0.75
