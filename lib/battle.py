"队伍相关，包括队伍创建。战斗相关，包括行动条，鬼火条，大宝剑，双方队伍的维护"
from random import choice
from servant_ import Scarecrow

class Team:
    "队伍类"
    def __init__(self):
        super().__init__()
        self.members = []
        self.energe = 4
        self.energe_circle = 0
        self.pet = None # 召唤物位
        self.center = None # 中位，也就是阴阳师/boss所在的位置
    
    def add_member(self, member):
        self.members.append(member)
        member.team = self
    
    def remove_member(self, member):
        if member in self.members:
            self.members.remove(member)
    
    def add_enemy(self, team):
        for member in self.members:
            member.enemy = team
    
    def set_arena(self, arena):
        self.arena = arena
    
    def alive_members(self):
        return [member for member in self.members if member.is_alive()]

    def random_member(self):
        if self.alive_members():
            return choice(self.alive_members())
    
    def best_choice(self):
        if isinstance(self.pet, Scarecrow):
            return self.pet
        return self.random_member()
    
    def energe_walk(self, num=1):
        self.energe_circle += num
        if self.energe_circle >= 5:
            self.energe_circle -= 5
            self.energe += 5
            if self.energe > 8:
                self.energe = 8
    
    def energe_change(self, num):
        self.energe += num
    
    def add_pet(self, pet):
        if self.pet is None:
            self.pet = pet
            self.add_member(pet)
    
    def remove_pet(self, pet):
        if self.pet is pet:
            self.pet = None
            self.remove_member(pet)

class Battle:
    "战斗类"
    def __init__(self):
        super().__init__()
        self.run_bar = None
        self.timer = 0
        self._ready = []
    
    def add(self, team1, team2):
        team1.add_enemy(team2)
        team2.add_enemy(team1)
        self.team1 = team1
        self.team1.set_arena(self)
        self.team2 = team2
        self.team2.set_arena(self)
        self.members = team1.members + team2.members
        self.members.sort(key=lambda x:x.status.get_speed(), reverse=True)
        self.run_bar = self.members[0].status.get_speed() * 30
        for each in self.members:
            each.config()
    
    def add_showtime(self, time):
        self.timer += time
    
    def run(self, time=360000):
        while self.timer < time and self.team1.alive_members() and self.team2.alive_members():

            while self._ready:
                self._ready.sort(key=lambda x:x.status.get_speed())
                actor = self._ready.pop()
                if actor.is_alive():
                    NormalRound(actor).run()

            for member in self.team1.members + self.team2.members:
                if member.is_alive():
                    member.move()
                    if member.location >= self.run_bar:
                        self._ready.append(member)

        if self.timer < time:
            if self.team1.alive_members():
                print("team1获胜")
            else:
                print("team2获胜")
        for each in self.members:
            print(each.recorder.get_result())

"""
实现式神的不同行动方式，正常回合，反击，伪回合。
"""
class Handler:
    "操控器基类"

    def __init__(self, actor):
        super().__init__()
        self.actor = actor

    def run(self):
        raise NotImplementedError

# TODO 回合开始阶段的过程
class PreAction(Handler):
    "回合前"

    def run(self):
        if not self.actor.is_alive():
            return
        # 记录行动次数
        self.actor.recorder.add_round()
        # 行动条重置为0
        self.actor.location = 0
        # 结算回合前触发的各种东西
        self.actor.trigger(self.actor, flag="action_pre_round")


# TODO 回合中的过程
class Acting(Handler):
    "回合中"

    def run(self):
        if not self.actor.is_alive():
            return
        # 选择技能，选择目标，使用技能
        self.actor.ai_act()

# TODO 回合后的过程
class Ending(Handler):
    "回合后"

    def run(self):
        if not self.actor.is_alive():
            return
        # 结算回合后的触发效果
        self.actor.trigger(self.actor, flag="action_post_round")
        # 自身buff降一层
        for each in self.actor.status_buff:
            each.layer_update()
        # 鬼火条推进一格
        if self.actor.classify != "召唤物":
            self.actor.team.energe_walk()
               

# 正常回合的过程
class NormalRound(Handler):
    "正常回合"

    def run(self):
        # 由三个回合组合而成
        PreAction(self.actor).run()
        Acting(self.actor).run()
        Ending(self.actor).run()


# TODO 反击回合的过程

class CounterRound(Handler):
    "反击回合"

    def run(self):
        pass

# TODO 伪回合的过程
class FakeRound(Handler):
    "伪回合"

    def run(self):
        pass