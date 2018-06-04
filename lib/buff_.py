"""
buff模块，包括各种增益减益等常时buff（例如星灭等）控制buff（由于伤害模拟用不到先不做）。 其他类似于土蜘蛛这种伤害buff待考虑。
生成buff实例所需要的参数：释放者caster，目标target
自有属性: id:buff的标识，用来判断是否有重复buff(从100开始），layer：层数;coexist_num: 可以同时存在的相同id的buff的个数
buff提供如下方法：add:将生成的buff实例添加到target的buff_list里， remove:删除target的buff_list里的self，layer_update: 在回合后用来更新层数
"""

class baseBuff:
    "buff基类"
    def __init__(self, caster):
        super().__init__()
        self.caster = caster
        self.config()
    
    def __repr__(self):
        return "{}{}".format(self.__class__, self.layer)
    
    def __eq__(self, obj):
        return isinstance(obj, type(self)) and self.caster == obj.caster
        
    def config(self):
        self.coexist_num = 100
        self.id = None
        self.layer = 1

    def add(self, target):
        self.target = target
        self.position = target.status_buff
        same_buffs = [buff for buff in self.position if buff == self]
        if len(same_buffs) < self.coexist_num:
            self.position.append(self)
            self._valid()
        else:
            same_buffs[0].remove()
            self.add(target)

    def _valid(self):
        # 生效过程，由子类实现
        raise NotImplementedError
    
    def remove(self):
        self._invalid()
        self.position.remove(self)
    
    def _invalid(self):
        # 反生效过程，由子类实现
        raise NotImplementedError

    def layer_update(self):
        self.layer -= 1
        if self.layer <= 0:
            self.remove()

class StatusBuff(baseBuff):
    "增益buff"
    pass

class StatusDebuff(baseBuff):
    "减益buff"
    def add(self, target):
        if not target.immune:
            super().add(target)

class Xing(StatusBuff):
    "晴明星，ID 100"
    def config(self):
        self.coexist_num = 1
        self.id = 100
        self.layer = 3
    
    def _valid(self):
        self.target.change_damage_ratio(+0.3)
    
    def _invalid(self):
        self.target.change_damage_ratio(-0.3)

class Mie(StatusDebuff):
    "晴明灭, ID 101"
    def config(self):
        self.coexist_num = 1
        self.id = 101
        self.layer = 3
    
    def _valid(self):
        self.target.change_harm_ratio(+0.3)
    
    def _invalid(self):
        self.target.change_harm_ratio(-0.3)

class SteelMao(StatusBuff):
    "天狗的钢铁毛 ID 102"
    def config(self):
        self.coexist_num = 1
        self.id = 102
        self.layer = 1
    
    def _valid(self):
        self.target.change_atk_ratio(0.15)
        self.target.change_extra_criDM(15)
    
    def _invalid(self):
        self.target.change_atk_ratio(-0.15)
        self.target.change_extra_criDM(-15)

class CurseFire(StatusDebuff):
    "丑女咒火 ID 103"
    def config(self):
        self.coexist_num = 1
        self.id = 103
        self.layer = 2
    
    def _valid(self):
        self.target.change_harm_ratio(+0.15)
    
    def _invalid(self):
        self.target.change_harm_ratio(-0.15)

class FuriousEyes(StatusDebuff):
    "两面佛怒目 ID 104"
    def config(self):
        self.coexist_num = 1
        self.id = 104
        self.layer = 2
    
    def _valid(self):
        self.target.change_atk_ratio(0.16)
        self.target.change_def_ratio(0.16)
    
    def _invalid(self):
        self.target.change_atk_ratio(-0.16)
        self.target.change_def_ratio(-0.16)

class Fear(StatusBuff):
    "陆生的畏 ID 105"
    def config(self):
        self.coexist_num = 4
        self.id = 105
        self.layer = 4
    
    def _valid(self):
        self.target.change_damage_ratio(+0.75)
    
    def _invalid(self):
        self.target.change_damage_ratio(-0.75)

class IndirectDM(baseBuff):
    "间接伤害buff ID为特有数字99"
    def config(self):
        self.coexist_num = 65535
        self.id = 99
        self.position = self.target.trigger_post_round
    
    def set_damage(self, damage):
        self.damage = damage
    
    def action(self):
        self.damage.set_defender(self.target)
        self.damage.get_result()
        self.target.defend(self.damage)
        self.remove()
    
    def _valid(self):
        pass
    
    def _invalid(self):
        pass