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
        # 行动条重置为0
        self.actor.location = 0
        # 结算回合前触发的各种东西
        for each in self.actor.trigger_pre_round:
            each.action()

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
        for each in self.actor.trigger_post_round:
            each.action()
        # 自身buff降一层
        for each in self.actor.status_buff:
            each.update_layer()
        # 鬼火条推进一格
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