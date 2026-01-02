from .building import Building


class SportsHall(Building):
    """ Зал для тренировок """
    
    def __init__(self):
        super().__init__()
        self.name = "sports_hall"
        