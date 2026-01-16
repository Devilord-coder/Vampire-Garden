import arcade
from os import listdir


class Enemy(arcade.Sprite):
    def __init__(
        self, scaling: float = 1, health: int = 100,
        folder_name: str = "skeleton", walk_speed: int = 0,
        fly_jump_speed: int = 0
    ):
        super().__init__()
        
        self.scale = scaling
        self.health = health
        
        self.name = folder_name
        
        self.change_x = walk_speed
        self.change_y = fly_jump_speed
        
        self.current_texture = 0
        self.texture_change_time = 0
        self.texture_change_delay = 0.3  # секунд на кадр
        
        self.boundary_right = self.boundary_left = self.boundary_top = self.boundary_bottom = 0
        
        self.textures_init()
        
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
        self.walk_b_textures = self.walk_f_textures # заглушка
        
        
    def update(self, delta_time):
        """ Перемещение персонажа """
        
        if self.change_x:
            self.walking = True
        
        if self.center_x <= self.boundary_left or self.center_x >= self.boundary_right:
            self.change_x = -self.change_x
        if self.center_y <= self.boundary_bottom or self.center_y >= self.boundary_top:
            self.change_y = -self.change_y
        
        self.update_animation(delta_time)
        
    def update_animation(self, delta_time):
        """ Обновление анимации """
        
        if self.walking:
            if self.change_x > 0:
                self.texture_change_time += delta_time
                if self.texture_change_time >= self.texture_change_delay:
                    self.texture_change_time = 0
                    self.current_texture += 1
                    if self.current_texture >= len(self.walk_f_textures):
                        self.current_texture = 0
                    self.texture = self.walk_f_textures[self.current_texture]
            else:
                self.texture_change_time += delta_time
                if self.texture_change_time >= self.texture_change_delay:
                    self.texture_change_time = 0
                    self.current_texture += 1
                    if self.current_texture >= len(self.walk_b_textures):
                        self.current_texture = 0
                    self.texture = self.walk_b_textures[self.current_texture]
        else:
            self.texture_change_time += delta_time
            if self.texture_change_time >= self.texture_change_delay:
                self.texture_change_time = 0
                self.current_texture += 1
                if self.current_texture >= len(self.idle_textures):
                    self.current_texture = 0
                self.texture = self.idle_textures[self.current_texture]
    
    def hurt(self, damage):
        """ Получение урона """
        
        self.health -= damage
        if self.health <= 0:
            self.death()
    
    def death(self):
        """ Смерть """
        
        ...