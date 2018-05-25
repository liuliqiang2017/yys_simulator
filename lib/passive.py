"""
被动技能以及御魂类
act_period：触发时间，数值从1-9，分别如下
    1. 回合开始前触发，比如大天狗的加攻击，作用于owner
    2. 攻击前触发，比如雪童子的冰冻，作用于damage
    3. 攻击时触发不管有没有伤害，比如网切， 作用于damage
    4. 攻击时有伤害触发(相当于攻击后)， 破势，针女，各种控制御魂，作用于damage
    5. 回合结束时触发，比如招财猫，轮入道等，作用于owner
    6. 受到攻击后触发（有伤害），金刚经，返魂香，铮，还有一些反击等。
注：觉醒带来的效果直接写入基础属性里，不单独作为被动技能实现。有些和技能挂钩的直接写在技能里，也不单独实现
action: 触发过程
"""

# TODO 基类
# TODO 被动技能类
# TODO 御魂类
# TODO 被动技能：天狗的钢铁毛，鸟的协战， 陆生的反击， 丑女的诅咒， 荒的开幻境， 酒吞的攒气
# TODO 御魂： 针女，网切，破势，招财猫，土蜘蛛。