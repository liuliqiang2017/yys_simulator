"""
一些奇怪机制的实现时用的小东西，比如协战，书翁的记仇，本体+两个分体。 犬神的反击，3个守护分体+1个反击本体。
不过当前只做和伤害有关的实现, 用观察者模式实现
"""
from passive import basePassive

class Event(basePassive):
    "事件类"

class Observer(basePassive):
    "观察者类"
    pass

# TODO 荒的幻境协战
# TODO 鸟的协战
# TODO 书翁记仇。
# TODO 土蜘蛛的效果