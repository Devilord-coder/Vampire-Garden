import arcade
import random

from src.settings import settings

RABBIT_SCALE = 5
RUN_SPEED = 130
ANIMATION_DELAY = 0.1


class Rabbit(arcade.Sprite):
    """Спрайт кролика"""

    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        """Подготовка спрайта"""
        self.left_walk_textures = []
        self.right_walk_textures = []
        self.left_run_textures = []
        self.right_run_textures = []
        self.idle_textures = []

        self.current_frame = 0
        self.animation_time = 0
        
        self.visible_time = 0
        self.max_visible_time = random.randint(30, 60)
        
        self.eat_time = 0
        self.max_eat_time = random.randint(15, 30)
        self.busy_field = None
        self.target_x = 0
        self.eat_stop = False

        self.direction = "left"
        self.state = "walk"

        self.center_x = settings.width + 50
        self.scale = RABBIT_SCALE
        self.speed = random.randint(-60, -30)
        self.start = True
        self.hungry = True

        self.fill_textures("walk", "left", 5)
        self.fill_textures("walk", "right", 5)
        self.fill_textures("run", "left", 6)
        self.fill_textures("run", "right", 6)
        self.fill_textures('idle', None, 4)
        self.texture = self.left_walk_textures[0]

    def fill_textures(self, state, direction, quantity_textures):
        """Заполнение списков текстур правильными текстурами"""
        for i in range(quantity_textures):
            if state == 'idle':
                texture = arcade.load_texture(f"resources/Minions/Rabbit/idle/sprite_0_{i}.png")
                self.idle_textures.append(texture)
            else:
                texture = arcade.load_texture(
                    f"resources/Minions/Rabbit/{state}/{direction}_{state}/sprite_0_{i}.png"
                )
            if state == "walk" and direction == "left":
                self.left_walk_textures.append(texture)
            elif state == "walk" and direction == "right":
                self.right_walk_textures.append(texture)
            elif state == "run" and direction == "left":
                self.left_run_textures.append(texture)
            elif state == "run" and direction == "right":
                self.right_run_textures.append(texture)

    def update(self, delta_time):
        """Обновление горизонтальной координаты, смена направления при достижении краёв, удаление, если убежал"""
        self.center_x += self.speed * delta_time
        self.update_animation(delta_time)
        
        if self.start and self.right >= settings.width:
            return
        elif self.start:
            self.start = False
            
        if self.state == "walk":
            if self.left <= 0:
                self.speed *= -1
                self.direction = "right"
            elif self.right >= settings.width:
                self.speed *= -1
                self.direction = "left"
        elif self.state == 'run':
            if self.speed == 0:
                if self.direction == 'left':
                    self.speed = -RUN_SPEED
                else:
                    self.speed = RUN_SPEED
            if self.right <= 0:
                self.remove_from_sprite_lists()
            elif self.left >= settings.width:
                self.remove_from_sprite_lists()
        elif self.state == 'idle':
            if self.eat_stop:
                self.eat_time += delta_time
                self.busy_field.time_with_rabbit += delta_time
                if self.eat_time >= self.max_eat_time:
                    self.busy_field.time_with_rabbit = 0
                    self.eat_time = 0
                    self.busy_field.busy = False
                    self.busy_field = None
                    self.eat_stop = False
                    self.state = 'run'
                    self.speed = RUN_SPEED
                    if self.direction == 'left':
                        self.speed *= -1
            else:
                if (self.target_x - abs(self.speed * delta_time)) <= self.center_x <= (self.target_x + abs(self.speed * delta_time)):
                    self.speed = 0
                    self.eat_stop = True
        
        self.visible_time += delta_time
        if self.visible_time >= self.max_visible_time and self.hungry:
            self.state = 'run'
            if self.direction == 'right':
                self.speed = RUN_SPEED
            elif self.direction == 'left':
                self.speed = -RUN_SPEED

    def update_animation(self, delta_time):
        """Обновление тектуры в зависимости от напрваления и состояния"""
        self.animation_time += delta_time

        if self.animation_time >= ANIMATION_DELAY:
            self.animation_time = 0
            texture_list = self.current_textures_list()
            self.current_frame = (self.current_frame + 1) % len(texture_list)
            self.texture = texture_list[self.current_frame]

    def current_textures_list(self):
        """Возврат списка текстур по направлению и состоянию"""
        if self.state == "walk":
            if self.direction == "left":
                return self.left_walk_textures
            elif self.direction == "right":
                return self.right_walk_textures

        elif self.state == "run":
            if self.direction == "left":
                return self.left_run_textures
            elif self.direction == "right":
                return self.right_run_textures
            
        elif self.state == 'idle':
            if self.eat_stop:
                return self.idle_textures
            if self.direction == 'left':
                return self.left_walk_textures
            elif self.direction == 'right':
                return self.right_walk_textures
