"测试模块"
from lib import battle
from lib import servant
from lib.passive_ import Needle, BadThing, LuckyCat, NetCut, DustSpider

def main():
    atk_dict = {"hp":28681, "atk":3427, "cri":100, "criDM":231, "speed":125, "def_":567, "yuhun":[], "name": "书翁"}
    atker = servant.ShuWeng(atk_dict)
    atk_dict1 = {"hp":21200, "atk":2558, "cri":105, "criDM":211, "speed":117, "def_":735, "yuhun":[LuckyCat], "name": "蜜桃"}
    atker1 = servant.Peach(atk_dict1)
    atk_dict2 = {"hp":13312, "atk":7256, "cri":105, "criDM":267, "speed":121.5, "def_":523, "yuhun":[BadThing], "name": "酒吞"}
    atker2 = servant.WineKing(atk_dict2)
    atk_dict3 = {"hp":17800, "atk":2770, "cri":44, "criDM":165, "speed":131, "def_":523, "yuhun":[BadThing, DustSpider], "name": "丑女"}
    atker3 = servant.UglyGirl(atk_dict3)
    atk_dict4 = {"hp":15300, "atk":8030, "cri":105, "criDM":277, "speed":121, "def_":523, "yuhun":[BadThing], "name": "陆生"}
    atker4 = servant.LuSheng(atk_dict4)
    def_dict = {"hp":20000000, "atk":1000, "cri":100, "criDM":100, "speed":130, "def_":300, "yuhun":[Needle]}
    defer1 = servant.Bird(def_dict)
    defer2 = servant.Bird(def_dict)
    defer1.name = "大天狗1"
    defer1.immune = True
    defer2.name = "大天狗2"

    team1 = battle.Team()
    team1.add_member(atker)
    team1.add_member(atker1)
    team1.add_member(atker2)
    team1.add_member(atker3)
    team1.add_member(atker4)
    team1.add_member(servant.QingMing())

    team2 = battle.Team()
    team2.add_member(defer1)
    team2.add_member(defer2)
    
    bat = battle.Battle()
    bat.add(team1, team2)

    result = bat.run()
    print(result)

if __name__ == '__main__':
    # import cProfile
    # test= "main()"
    # cProfile.run(test)
    main()