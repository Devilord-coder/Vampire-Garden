from .building import Building


class SkeletonHouse(Building):
    """ Дом скелета """
    
    def __init__(self):
        super().__init__()
        self.name = "skeleton_house"


skeleton_house = SkeletonHouse()