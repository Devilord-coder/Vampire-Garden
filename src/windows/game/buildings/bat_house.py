import arcade
from .building import Building


class BatHouse(Building):
    """Дом летучей мыши"""

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.name = "bat_house"
        self.req_list = [
            {"estate": 1},
            {"estate": 2},
            {"estate": 3},
            {"estate": 4},
            {"estate": 5},
            {"estate": 6},
        ]
        self.textures = []
        self.fill_textures()
        self.building_init("bat", self.textures)  # Метод родителя

    def fill_textures(self):
        """Метод загрузки текстур бойца для переключения"""
        for i in range(18):
            number = str(i)
            number = number.rjust(3, "0")
            texture = arcade.load_texture(
                f"resources/Minions/Vampire_Bat/PNG/PNG Sequences/Fly/0_Monster_Fly_{number}.png"
            )
            self.textures.append(texture)
