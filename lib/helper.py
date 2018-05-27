"""
一些奇怪机制的实现时用的小东西，比如协战，书翁的记仇，本体+两个分体。 犬神的反击，3个守护分体+1个反击本体。
不过当前只做和伤害有关的实现, 用观察者模式实现
"""
from random import randint
from damage_ import NoteDamage

class Linker:
    "联动器基类"
    def __init__(self, owner):
        self.owner = owner
        self._link = []
        self.config()
    
    def config(self):
        self.position = "self.target.trigger_pre_round"
    
    def link_to(self, link):
        if link not in self._link:
            self._link.append(link)
        if self not in link._link:
            link._link.append(self)
    
    def link_cut(self, link):
        self._link.remove(link)
        link.link_cut(self)
    
    def add(self, target):
        self.target = target
        self.position = eval(self.position)
        self.position.append(self)
    
    def remove(self):
        self.position.remove(self)
    
    def action(self):
        raise NotImplementedError


class AssistAtk(Linker):
    "协战, 把观察者放在每个其他友方式神的触发里"
    def config(self):
        self.chance = 300
    
    def add(self, target):
        for each in target.team.members:
            if each is not self.owner:
                each.trigger_post_skill.append(self)

    def remove(self):
        for each in self.owner.team.members:
            if each is not self.owner:
                each.trigger_post_skill.remove(self)
    
    def action(self, damage):
        if all([self.owner.is_alive(),
               damage.skill_id == 1,
               randint(1, 1000) <= self.chance]):
            self.owner.assist(damage.defer)

# 荒的幻境协战
class HuangAssist(AssistAtk):
    "荒的协战"
    def config(self):
        self.chance = 500
    
    def action(self, damage):
        if self.owner.aura:
            super().action(damage)


# 鸟的协战
class BirdAssist(AssistAtk):
    "鸟的协战"
    def config(self):
        self.chance = 300

# 书翁记仇。
class TakeNotes(Linker):
    "书翁记仇的分体, 主体作为被动存在"
    def config(self):
        self.dm_memo = 0
        self.position = "self.target.trigger_by_hit"
        self.link_to(self.owner.notebook)
    
    def action(self, damage):
        self.dm_memo += damage.val
    
    def explode(self):
        dm = NoteDamage(self.owner)
        dm.set_defender(self.target)
        dm.set_base_val(self.dm_memo)
        dm.run()
        self.remove()

class Notebook(Linker):
    "书翁记仇的主体"
    
    def action(self):
        for each in self._link:
            each.explode()
            self._link.remove(each)
    
    
# TODO 土蜘蛛的效果