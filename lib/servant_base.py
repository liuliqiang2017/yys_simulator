"存储一些式神的初始数据"
import passive
import helper

BOSS_DUMMY = {"base_atk" : 3000,
              "base_def" : 300,
              "base_speed" : 120,
              "base_cri" : 50,
              "base_criDM" : 150,
              "base_max_hp" : 20000000,
              "passive":[]}

BigDog = {    "base_atk" : 3136,
              "base_def" : 419,
              "base_speed" : 110,
              "base_cri" : 10,
              "base_criDM" : 150,
              "base_max_hp" : 10026,
              "passive":[passive.SteelFeather]}

Bird = {      "base_atk" : 3082,
              "base_def" : 397,
              "base_speed" : 113,
              "base_cri" : 10,
              "base_criDM" : 150,
              "base_max_hp" : 10823,
              "passive":[helper.BirdAssist]}

WineKing = {  "base_atk" : 3136,
              "base_def" : 375,
              "base_speed" : 113,
              "base_cri" : 10,
              "base_criDM" : 150,
              "base_max_hp" : 11165,
              "passive":[passive.DrinkByHit, passive.DrinkPostRound]}

LuSheng = {   "base_atk" : 3028,
              "base_def" : 384,
              "base_speed" : 113,
              "base_cri" : 10,
              "base_criDM" : 150,
              "base_max_hp" : 11393,
              "passive":[]}

YuZaoQian = { "base_atk" : 3350,
              "base_def" : 353,
              "base_speed" : 110,
              "base_cri" : 12,
              "base_criDM" : 160,
              "base_max_hp" : 12532,
              "passive":[]}

ShuWeng = {   "base_atk" : 2680,
              "base_def" : 441,
              "base_speed" : 109,
              "base_cri" : 8,
              "base_criDM" : 150,
              "base_max_hp" : 11393,
              "passive":[helper.Notebook]}