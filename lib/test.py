"测试模块"
import battle
from servant import Servant, BigDog, Bird, LuSheng
from handler import NormalRound
from passive import Needle, BadThing, LuckyCat, NetCut

def main():
    atk_dict = {"hp":100000, "atk":8312, "cri":105, "criDM":257, "speed":135, "def_":523, "yuhun":[Needle], "name": "陆生"}
    atker = LuSheng(atk_dict)
    atk_dict1 = {"hp":100000, "atk":8812, "cri":105, "criDM":227, "speed":128, "def_":523, "yuhun":[Needle], "name": "姑获鸟"}
    atker1 = Bird(atk_dict1)
    atk_dict2 = {"hp":100000, "atk":8812, "cri":105, "criDM":227, "speed":125, "def_":523, "yuhun":[Needle], "name": "大天狗"}
    atker2 = BigDog(atk_dict2)
    def_dict = {"hp":400000, "atk":1000, "cri":100, "criDM":100, "speed":110, "def_":300, "yuhun":[]}
    defer1 = Servant(def_dict)
    defer2 = Servant(def_dict)
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