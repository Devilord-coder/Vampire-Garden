import arcade
import random


class Participle(arcade.SpriteCircle):
    """Класс для создания частиц"""

    def __init__(self, x, y):
        color = random.choice(
            [
                (200, 200, 200, 200),
                (180, 180, 180, 200),
                (220, 220, 220, 200),
                (190, 170, 150, 200),
            ]
        )
        size = random.randint(3, 8)
        super().__init__(size, color)
        self.center_x = x
        self.center_y = y
        self.change_x = random.uniform(-1.5, 1.5)
        self.change_y = random.uniform(0, 2)
        self.scale = 1.0
        self.alpha = 200
        self.lifetime = random.uniform(0.5, 1.2)
        self.time_alive = 0

    def update(self, delta_time):
        """Обновление частицы"""
        self.center_x += self.change_x
        self.center_y += self.change_y

        self.change_x *= 0.95
        self.change_y *= 0.95

        self.scale_x *= 1.02
        self.scale_y *= 1.005

        self.alpha -= 2

        self.time_alive += delta_time

        if self.time_alive >= self.lifetime:
            self.remove_from_sprite_lists()
