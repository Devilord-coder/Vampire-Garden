from .building import Building


class WerewolfHouse(Building):
    """ Дом оборотней """
    
    def __init__(self):
        super().__init__()
        self.name = "werewolf_house"
        

werewolf_house = WerewolfHouse()