import arcade
from .building import Building


class SkeletonHouse(Building):
    """Дом скелета"""

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.name = "skeleton_house"

        self.textures = []
        self.fill_textures()
        self.building_init("sceleton", self.textures)  # Метод родителя

    def fill_textures(self):
        """Метод загрузки текстур бойца для переключения"""
        for i in range(7):
            
            texture = arcade.load_texture(
                f"resources/Minions/Skeleton_Spearman/Walk/sprite_0_{i}.png"
            )
            self.textures.append(texture)
