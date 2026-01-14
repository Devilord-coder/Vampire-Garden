import arcade
from os import listdir


class FireBoll(arcade.Sprite):
    """ Класс огненных шаров """
    
    def __init__(self, scale = 1,
                 center_x = 0, center_y = 0,
                 change_x=3, change_y=0,
                 collision: list[arcade.SpriteList] | None = None):
        super().__init__()
        
        self.scale = scale
        
        self.center_x = center_x
        self.center_y = center_y
        self.change_x = 3
        self.change_y = 0
        
        self.collision_list = collision
        
        self.textures_init()
        
        self.attacking = False
        self.deleted = False
        
        self.current_texture = 0
        self.texture_change_time = 0
        self.texture_change_delay = 0.1  # секунд на кадр
    
    def textures_init(self):
        """ Инициализация тектур """
        
        self.fly_textures = []
        self.attack_textures = []
        
        for file_name in filter(lambda x: x[-4:] == ".png",
                                listdir("resources/Objects/fireboll/fly")):
            self.fly_textures.append(arcade.load_texture(f"resources/Objects/fireboll/fly/{file_name}"))
            
        for file_name in filter(lambda x: x[-4:] == ".png",
                                listdir("resources/Objects/fireboll/attack")):
            self.attack_textures.append(arcade.load_texture(f"resources/Objects/fireboll/attack/{file_name}"))
    
    def update(self, delta_time):
        """ Перемещение персонажа """
        
        if self.deleted:
            return
        
        for col_list in self.collision_list:
            if arcade.check_for_collision_with_list(self, col_list):
                self.attacking = True
                self.change_x = self.change_y = 0
                break
            
        self.center_x += self.change_x
        self.center_y += self.change_y
        
        self.update_animation(delta_time)
    
    def update_animation(self, delta_time):
        """ Обновление анимации """
        
        if not self.attacking:
            self.texture_change_time += delta_time
            if self.texture_change_time >= self.texture_change_delay:
                self.texture_change_time = 0
                self.current_texture += 1
                if self.current_texture >= len(self.fly_textures):
                    self.current_texture = 0
                self.texture = self.fly_textures[self.current_texture]
        else:
            self.texture_change_time += delta_time
            if self.texture_change_time >= self.texture_change_delay:
                self.texture_change_time = 0
                self.current_texture += 1
                if self.current_texture >= len(self.attack_textures):
                    self.deleted = True
                else:
                    self.texture = self.attack_textures[self.current_texture]
