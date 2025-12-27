from .building import Building


class BatHouse(Building):
    """ Дом летучей мыши """
    
    def __init__(self):
        super().__init__()
        self.name = "bat_house"
        self.req_list = [
            {
                "estate": 1
            },
            {
                "estate": 2
            },
            {
                "estate": 3
            },
            {
                "estate": 4
            },
            {
                "estate": 5
            },
            {
                "estate": 6
            },
        ]


bat_house = BatHouse()