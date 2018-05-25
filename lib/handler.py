"""
实现式神的不同行动方式，正常回合，反击，伪回合。
"""
# TODO 回合开始阶段的过程
class PreAction:
    "回合前"
    def __init__(self, actor):
        super().__init__()
        self.actor = actor
    
    def run(self):
        # 行动条重置为0
        self.actor.location = 0
        # 结算幻境类
        self.actor.teambuff
        # 结算伤害类buff
        # 结算自身被动

# TODO 回合中的过程
# TODO 回合后的过程
# TODO 正常回合的过程
# TODO 反击回合的过程
# TODO 伪回合的过程