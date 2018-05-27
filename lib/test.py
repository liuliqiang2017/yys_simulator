"测试模块"
import battle
from servant import Servant, BigDog, Bird, WineKing
from handler import NormalRound
from passive import Needle, BadThing, LuckyCat

def main():
    atk_dict = {"hp":100000, "atk":8312, "cri":105, "criDM":197, "speed":135, "def_":523, "yuhun":[Needle]}
    atker = WineKing(atk_dict)
    atk_dict1 = {"hp":100000, "atk":5812, "cri":105, "criDM":267, "speed":175, "def_":523, "yuhun":[Needle]}
    atker1 = Bird(atk_dict1)
    def_dict = {"hp":2000000, "atk":1000, "cri":100, "criDM":100, "speed":60, "def_":300, "yuhun":[]}
    defer1 = Servant(def_dict)
    defer2 = Servant(def_dict)
    defer1.name = "狮子1"
    defer1.max_hp = defer1.hp = 500
    defer2.name = "狮子2"

    team1 = battle.Team()
    team1.add_member(atker)
    team1.add_member(atker1)

    team2 = battle.Team()
    team2.add_member(defer1)
    team2.add_member(defer2)
    
    bat = battle.Battle()
    bat.add(team1, team2)

    bat.run()

if __name__ == '__main__':
    main()