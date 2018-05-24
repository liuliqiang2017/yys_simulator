"""
buff模块，包括各种增益减益等常时buff（例如星灭等）控制buff（由于伤害模拟用不到先不做）。 其他类似于土蜘蛛这种伤害buff待考虑。
生成buff实例所需要的参数：释放者caster，目标target
自有属性layer：层数， update_period：层数更新时间，有3个值：1-回合前，2-攻击时， 3-回合后
buff提供如下方法：add:将生成的buff实例添加到target的buff_list里， remove:删除target的buff_list里的self，
"""

class StatusBuff:
    "属性buff基类"
    def __init__(self, caster, target):
        super().__init__()
        self.caster = caster
        self.target = target
        self.layer = None
        self.update_period = None

    def add(self):
        self.target.buffs.append(self)
        self._valid()
    
    def _valid(self):
        raise NotImplementedError
    
    def remove(self):
        self.target.buffs.remove(self)
        self._invalid()
    
    def _invalid(self):
        raise NotImplementedError

    def layer_update(self):
        raise NotImplementedError
