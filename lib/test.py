"测试模块"
import battle
from servant import Servant
from handler import NormalRound
from passive import Needle, BadThing, LuckyCat

def main():
    atk_dict = {"hp":100000, "atk":2000, "cri":50, "criDM":300, "speed":100, "def_":300, "yuhun":[Needle, BadThing, LuckyCat]}
    atker = Servant(atk_dict)
    atker.name = "老虎"
    def_dict = {"hp":200000, "atk":1000, "cri":100, "criDM":100, "speed":60, "def_":300, "yuhun":[]}
    defer1 = Servant(def_dict)
    defer2 = Servant(def_dict)
    defer1.name = "狮子1"
    defer1.max_hp = defer1.hp = 500
    defer2.name = "狮子2"

    team1 = battle.Team()
    team1.add_member(atker)

    team2 = battle.Team()
    team2.add_member(defer1)
    team2.add_member(defer2)
    
    bat = battle.Battle()
    bat.add(team1, team2)

    bat.run()

if __name__ == '__main__':
    main()