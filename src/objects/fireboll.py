import arcade
from src.registry import reg


class FireBoll(arcade.Sprite):
    """ Класс огненных шаров """
    
    def __init__(self, scale: float = 1,
                 center_x=0, center_y=0,
                 change_x=3, change_y=0,
                 collision: list[arcade.SpriteList] | None = None):
        super().__init__()
        
        """ Класс огненных шаров
        
        Args
        -------------------------
            scale: float = 1 - масштаб;
            center_x, center_y - координаты спрайта;
            change_x, change_y - скорость по x и y;
            collision: list[arcade.SpriteList] | None = None - список спрайтов,
            при столкновении с которыми шар взрывается
        """
        
        # основный параметры спрайта
        self.scale = scale
        self.center_x = center_x
        self.center_y = center_y
        self.change_x = change_x
        self.change_y = change_y
        
        # список спрайтов, с которыми нельзя сталкиваться
        self.collision_list = collision
        
        # список текстур
        self.fly_textures = reg.fireboll_fly_textures.copy()
        self.attack_textures = reg.fireboll_attack_textures.copy()
        # текущая текстура
        self.texture = self.fly_textures[0]
        
        # взрывается или нет
        self.attacking = False
        # уничтожен или нет
        self.deleted = False
        
        self.current_texture = 0
        self.texture_change_time = 0
        self.texture_change_delay = 0.1  # секунд на кадр
    
    def update(self, delta_time):
        """ Перемещение персонажа """
        
        if self.deleted:
            return
        
        # проверка на столкновение
        for col_list in self.collision_list:
            if arcade.check_for_collision_with_list(self, col_list):
                self.attacking = True
                self.change_x = self.change_y = 0
                break
            
        # перемещение
        self.center_x += self.change_x
        self.center_y += self.change_y
        
        # обновление анимации
        self.update_animation(delta_time)
    
    def update_animation(self, delta_time):
        """ Обновление анимации """
        
        if not self.attacking: # если не атакует
            self.texture_change_time += delta_time
            if self.texture_change_time >= self.texture_change_delay:
                self.texture_change_time = 0
                self.current_texture += 1
                if self.current_texture >= len(self.fly_textures):
                    self.current_texture = 0
                self.texture = self.fly_textures[self.current_texture]
        elif self.attacking:
            self.texture_change_time += delta_time
            if self.texture_change_time >= self.texture_change_delay:
                self.texture_change_time = 0
                self.current_texture += 1
                if self.current_texture >= len(self.attack_textures):
                    self.deleted = True
                else:
                    self.texture = self.attack_textures[self.current_texture]
