from .building import Building


class Library(Building):
    """ Здание библиотеки """
    
    def __init__(self):
        super().__init__()
        self.name = "library"


library = Library()