"宠物，召唤物等"
import servant
import servant_base
import skill_

class basePet(servant.Servant):
    "宠物类基类"
    def create(self):
        raise NotImplementedError

    def remove(self):
        raise NotImplementedError

class Scarecrow(basePet):
    "丑女的草人"
    def __init__(self, owner, target):
        self.owner = owner
        self.target = target
        data_dict = self.make_data_dict(target)
        super().__init__(data_dict)
        self.round_num = 2
        self.location = 0
    
    def make_data_dict(self, target):
        data_dict = target.data_dict
        data_dict["name"] = "草人"
        data_dict["hp"] = target.status.get_max_hp() * 0.3
        data_dict["speed"] = target.status.get_speed()
        data_dict["def_"] = target.status.def_ * 0.5
    
    def config(self):
        super().config(servant_base.Scarecrow)
        self.create()
    
    def create(self):
        self.target.team.add_pet(self)
    
    def remove(self):
        self.target.team.remove_per(self)