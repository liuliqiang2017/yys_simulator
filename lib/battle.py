"队伍相关，包括队伍创建。战斗相关，包括行动条，鬼火条，大宝剑，双方队伍的维护"
from handler import NormalRound

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
    
    def add_enemy(self, team):
        for member in self.members:
            member.enemy = team
    
    def alive_members(self):
        return [member for member in self.members if member.is_alive()]
    
    def energe_walk(self, num=1):
        self.energe_circle += num
        if self.energe_circle >= 5:
            self.energe_circle -= 5
            self.energe += 5
            if self.energe > 8:
                self.energe = 8
    
    def energe_change(self, num):
        self.energe += num

class Battle:
    "战斗类"
    def __init__(self):
        super().__init__()
        self.run_bar = None
        self._alive = True
        self._ready = []
    
    def add(self, team1, team2):
        team1.add_enemy(team2)
        team2.add_enemy(team1)
        self.team1 = team1
        self.team2 = team2
        self.members = team1.members + team2.members
        self.members.sort(key=lambda x:x.status.get_speed(), reverse=True)
        self.run_bar = self.members[0].status.get_speed() * 30
        for each in self.members:
            each.config()
    
    def run(self):
        while self.team1.alive_members() and self.team2.alive_members():

            while self._ready:
                self._ready.sort(key=lambda x:x.status.get_speed())
                NormalRound(self._ready.pop()).run()

            for member in self.members:
                member.move()
                if member.location >= self.run_bar:
                    self._ready.append(member)

        if self.team1.alive_members():
            print("team1获胜")
        else:
            print("team2获胜")
        for each in self.members:
            print(each.recorder.get_result())