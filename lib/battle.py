"队伍相关，包括队伍创建。战斗相关，包括行动条，鬼火条，大宝剑，双方队伍的维护"
from random import choice
from . import servant
from . import passive_
from . import config

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
        if isinstance(self.pet, servant.Scarecrow):
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
    
    def get_result(self):
        return [each.recorder_get_result() for each in self.members]

class Battle:
    "战斗类"
    def __init__(self):
        super().__init__()
        self.run_bar = None
        self.limit = 3600
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
        self.set_servant()
        self.set_run_bar()
    
    def set_servant(self):
        for each in self.members:
            each.initialize_servant()

    
    def set_run_bar(self):
        self.members.sort(key=lambda x:x.status.get_speed(), reverse=True)
        self.run_bar = self.members[0].status.get_speed() * 30

    def add_showtime(self, time):
        self.timer += time
    
    def who_win(self):
        return bool(self.team1.alive_members()) if self.timer < self.limit else None

    def get_result(self):
        return [self.who_win(), self.team1.get_result(), self.team2.get_result(), self.timer]
    
    def run(self):
        while self.timer < self.limit and self.team1.alive_members() and self.team2.alive_members():

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

        return self.get_result()

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
        self.actor.recorder_add_round()
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
        self.actor.update_buffs()
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

# 接收界面传过来的data数据，模拟战斗，返回结果

class Simulate:
    "模拟战斗类"
    def __init__(self, data):
        self.data = data
    
    def create_servant(self, data_dict):
        data = dict(
            name = data_dict["servant_name"],
            hp = data_dict["servant_hp"],
            speed = data_dict["servant_speed"],
            atk = data_dict["servant_atk"],
            def_ = data_dict["servant_def"],
            cri = data_dict["servant_cri"],
            criDM = data_dict["servant_cridm"],
            yuhun = []
        )

        data["yuhun"].append(self.get_servant_yuhun(data_dict, "servant_yuhun"))
        if "servant_yuhun_01" in data_dict:
            data["yuhun"].append(self.get_servant_yuhun(data_dict, "servant_yuhun_01"))
        return self.get_servant_cls(data_dict)(data)
    
    def get_servant_cls(self, data_dict):    
        cls_str = config.SERVANT_SOURCE[data_dict["servant_cls"]]["cls"]
        return eval("servant." + cls_str)
    
    def get_servant_yuhun(self, data_dict, key):
        yuhun_str = config.YUHUN_SOURCE[data_dict[key]]["cls"]
        return eval("passive_." + yuhun_str)
    
    def has_servant(self, data_dict):
        return data_dict["servant_cls"] is not None
    
    def create_team(self, start, end):
        team = Team()
        # 添加指定index的式神
        for i in range(start, end + 1):
            data_dict = self.data[str(i)]
            if self.has_servant(data_dict):
                team.add_member(self.create_servant(data_dict))
        return team

    def init_arena(self):
        # 建立队伍
        team1 = self.create_team(1, 5)
        team1.add_member(servant.QingMing())
        team2 = self.create_team(6, 10)
        # 建立竞技场
        arena = Battle()
        arena.add(team1, team2)
        return arena
    
    def run(self):
        arena = self.init_arena()
        return arena.run()