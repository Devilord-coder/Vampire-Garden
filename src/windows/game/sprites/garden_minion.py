import arcade
from src.settings import settings

SCALE = 3
SPEED = 100
ANIMATION_DELAY = 0.1


class GardenMinion(arcade.Sprite):
    """Класс персонажа для охраны огорода"""

    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        """Загрузка ресурсов, начальная настройка"""
        self.right_textures = []
        self.left_textures = []
        for i in range(8):
            texture = arcade.load_texture(
                f"resources/Minions/Vampire_Minion/Walk/sprite_0_{i}.png"
            )
            self.right_textures.append(texture)
            self.left_textures.append(texture.flip_horizontally())

        self.center_x = settings.width // 2
        self.center_y = settings.height // 2
        self.current_texture = 0
        self.texture = self.right_textures[self.current_texture]
        self.scale = SCALE
        self.speed = SPEED
        self.animation_time = 0
        self.direction = "right"
        self.pressed_keys = set()  # Клавиши, которые пользователь нажал

    def update(self, delta_time):
        """Обновление координат персонажа при ходьбе, смена направления взора при необходимости"""
        minion_go = False  # Проверка совершения движения для обновления анимации ходьбы
        if arcade.key.LEFT in self.pressed_keys:
            self.center_x -= self.speed * delta_time
            self.direction = "left"
            minion_go = True
        elif arcade.key.RIGHT in self.pressed_keys:
            self.center_x += self.speed * delta_time
            self.direction = "right"
            minion_go = True

        if arcade.key.UP in self.pressed_keys:
            self.center_y += self.speed * delta_time
            minion_go = True
        elif arcade.key.DOWN in self.pressed_keys:
            self.center_y -= self.speed * delta_time
            minion_go = True

        # Проверка выхода за пределы экрана
        if self.right >= settings.width:
            self.right = settings.width
        elif self.left <= -100:
            self.left = -100

        if self.top >= settings.height:
            self.top = settings.height
        elif self.bottom <= 30:
            self.bottom = 30

        if minion_go:
            self.update_animation(delta_time)

    def update_animation(self, delta_time):
        """Метод смены текстур при ходьбе с течением времени"""
        self.animation_time += delta_time

        if self.animation_time >= ANIMATION_DELAY:
            self.animation_time = 0
            texture_list = self.current_texture_list()
            self.current_texture = (self.current_texture + 1) % len(texture_list)
            self.texture = texture_list[self.current_texture]

    def current_texture_list(self):
        """Возврат нужных текстур персонажа в зависимости от направления взора"""
        if self.direction == "right":
            return self.right_textures
        elif self.direction == "left":
            return self.left_textures
