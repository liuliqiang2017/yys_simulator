"测试模块"
import battle
import servant_
from passive_ import Needle, BadThing, LuckyCat, NetCut

def main():
    atk_dict = {"hp":100000, "atk":8312, "cri":105, "criDM":257, "speed":135, "def_":523, "yuhun":[LuckyCat], "name": "书翁"}
    atker = servant_.ShuWeng(atk_dict)
    atk_dict1 = {"hp":100000, "atk":8812, "cri":105, "criDM":227, "speed":128, "def_":523, "yuhun":[Needle, BadThing], "name": "姑获鸟"}
    atker1 = servant_.Bird(atk_dict1)
    atk_dict2 = {"hp":100000, "atk":8812, "cri":105, "criDM":227, "speed":145, "def_":523, "yuhun":[BadThing], "name": "丑女"}
    atker2 = servant_.UglyGirl(atk_dict2)
    def_dict = {"hp":400000, "atk":1000, "cri":100, "criDM":100, "speed":110, "def_":300, "yuhun":[]}
    defer1 = servant_.Servant(def_dict)
    defer2 = servant_.Servant(def_dict)
    defer1.name = "狮子1"
    defer1.max_hp = defer1.hp = 500
    defer2.name = "狮子2"

    team1 = battle.Team()
    team1.add_member(atker)
    team1.add_member(atker1)
    team1.add_member(atker2)

    team2 = battle.Team()
    team2.add_member(defer1)
    team2.add_member(defer2)
    
    bat = battle.Battle()
    bat.add(team1, team2)

    bat.run()

if __name__ == '__main__':
    main()