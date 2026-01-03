import arcade
from .building import Building


class WerewolfHouse(Building):
    """Дом оборотней"""

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.name = "werewolf_house"

        self.textures = []
        self.fill_textures()
        self.building_init("werewolf", self.textures)  # Метод родителя

    def fill_textures(self):
        """Метод загрузки текстур бойца для переключения"""
        for i in range(11):
            texture = arcade.load_texture(
                f"resources/Minions/Werewolf/Walk/sprite_0_{i}.png"
            )
            self.textures.append(texture)
