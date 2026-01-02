from .building import Building


class Estate(Building):
    """ Здание поместья """
    
    def __init__(self):
        super().__init__()
        self.name = "estate"
