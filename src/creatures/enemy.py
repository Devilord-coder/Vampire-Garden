import arcade
from os import listdir


class Enemy(arcade.Sprite):
    def __init__(
        self, enemies_name_list: list = [], scaling: float = 1, health: int = 100,
        folder_name: str = "skeleton", walk_speed: int = 3,
        fly_jump_speed: int = 0, power: int = 25,
    ):
        super().__init__()
        
        self.scale = scaling
        
        # сила и здоровье
        self.power = power
        self.health = health
        
        self.enemies_name_list = enemies_name_list
        
        # название типа
        self.name = folder_name
        
        # скорость по x и y
        self.change_x = walk_speed
        self.change_y = fly_jump_speed
        
        # умер или нет
        self.death = False
        self.attacking = False
        
        self.current_texture = 0
        self.texture_change_time = 0
        self.texture_change_delay = 0.2  # секунд на кадр
        
        # границы передвижения
        self.boundary_right = self.boundary_left = self.boundary_top = self.boundary_bottom = 0
        
        # инициализация текстур
        self.textures_init()
        
        # текущая текстура
        self.texture = self.idle_textures[0]
    
    def textures_init(self):
        """ Подключение внешнего вида персонажа """
        
        # неподвижный режим
        self.idle_textures = []
        for name in listdir(f"resources/Enemies/{self.name}/idle"):
            if name[-4:] == ".png":
                texture = arcade.load_texture(f"resources/Enemies/{self.name}/idle/{name}")
                self.idle_textures.append(texture)
        
        # передвижение
        self.walk_f_textures = []
        for name in listdir(f"resources/Enemies/{self.name}/walk_forward"):
            if name[-4:] == ".png":
                texture = arcade.load_texture(f"resources/Enemies/{self.name}/walk_forward/{name}")
                self.walk_f_textures.append(texture)
        # передвижение назад
        self.walk_b_textures = []
        for name in listdir(f"resources/Enemies/{self.name}/walk_back"):
            if name[-4:] == ".png":
                texture = arcade.load_texture(f"resources/Enemies/{self.name}/walk_back/{name}")
                self.walk_b_textures.append(texture)
        
        self.death_textures = []
        for name in sorted(listdir(f"resources/Enemies/{self.name}/death")):
            if name[-4:] == ".png":
                texture = arcade.load_texture(f"resources/Enemies/{self.name}/death/{name}")
                self.death_textures.append(texture)
        
        self.attack_textures = []
        for name in sorted(listdir(f"resources/Enemies/{self.name}/attack")):
            if name[-4:] == ".png":
                texture = arcade.load_texture(f"resources/Enemies/{self.name}/attack/{name}")
                self.attack_textures.append(texture)
        
        
    def update(self, delta_time):
        """ Перемещение персонажа """
        
        if self.change_x:
            self.walking = True
        
        if self.center_x <= self.boundary_left or self.center_x >= self.boundary_right:
            self.change_x = -self.change_x
        if self.center_y <= self.boundary_bottom or self.center_y >= self.boundary_top:
            self.change_y = -self.change_y
        
        self.update_animation(delta_time)
    
    def attack(self):
        self.attacking = True
        self.current_texture = -1
        
    def update_animation(self, delta_time):
        """ Обновление анимации """
        
        self.texture_change_time += delta_time
        
        if self.death:
            if self.texture_change_time >= self.texture_change_delay:
                self.texture_change_time = 0
                self.current_texture += 1
                if self.current_texture >= len(self.death_textures):
                    self.kill()
                else:
                    self.texture = self.death_textures[self.current_texture]
        elif self.attacking:
            if self.texture_change_time >= self.texture_change_delay:
                self.texture_change_time = 0
                self.current_texture += 1
                if self.current_texture >= len(self.attack_textures):
                    self.attacking = False
                    self.current_texture = -1
                else:
                    self.texture = self.attack_textures[self.current_texture]
        elif self.walking:
            if self.change_x > 0:
                if self.texture_change_time >= self.texture_change_delay:
                    self.texture_change_time = 0
                    self.current_texture += 1
                    if self.current_texture >= len(self.walk_f_textures):
                        self.current_texture = 0
                    self.texture = self.walk_f_textures[self.current_texture]
            else:
                if self.texture_change_time >= self.texture_change_delay:
                    self.texture_change_time = 0
                    self.current_texture += 1
                    if self.current_texture >= len(self.walk_b_textures):
                        self.current_texture = 0
                    self.texture = self.walk_b_textures[self.current_texture]
        else:
            if self.texture_change_time >= self.texture_change_delay:
                self.texture_change_time = 0
                self.current_texture += 1
                if self.current_texture >= len(self.idle_textures):
                    self.current_texture = 0
                self.texture = self.idle_textures[self.current_texture]
    
    def hurt(self, damage):
        """ Получение урона """
        
        self.health -= damage
        if self.health <= 0 and not self.death:
            self.death = True
            self.current_texture = -1
            self.enemies_name_list.append(self.name)
            self.change_x = self.change_y = 0