import arcade
from src.objects import FireBoll


class Hero(arcade.Sprite):
    def __init__(
        self, scaling=1.2, walk_speed=3,
        run_speed=5, jump_speed=10
    ):
        super().__init__()
        
        self.scale = scaling
        
        # Основные характеристики
        self.health = 100
        self.walk_speed = walk_speed
        self.run_speed = run_speed
        self.jump_speed = jump_speed
        
        self.create_vampire_textures()
        
        # Загрузка текстур
        self.texture = self.idle_textures[0]
            
        self.current_texture = 0
        self.texture_change_time = 0
        self.texture_change_delay = 0.1  # секунд на кадр
        
        # ---- Параметры состояния персонажа ----
        # идет вперед
        self.walk_f = False
        # идет назад
        self.walk_b = False
        # получает ли урон
        self.hurting = False
        # умер ли
        self.dead = False
        # является ли летучей мышью
        self.bat = False
        # атакует назад или вперед
        self.attack_f = self.attack_b = False
        # Персонаж не может двигаться
        self.disabled = False
    
    def create_bat_textures(self):
        """ Изменение внешнего вида на летучую мышь """
        
        # неподвижный режим
        self.idle_textures = []
        # ходьба вперед
        self.walk_f_textures = []
        for i in range(18):
            texture = arcade.load_texture(f"resources/Hero/bat/walk_forward/{i}.png")
            self.walk_f_textures.append(texture)
        # ходьба назад
        self.walk_b_textures = []
        self.walk_b_textures = self.idle_textures = self.walk_f_textures
        # получение урона
        self.hurt_textures = self.idle_textures # заглушка
        # смерть
        self.death_textures = []
        for i in range(18):
            texture = arcade.load_texture(f"resources/Hero/bat/death/{i}.png")
            self.death_textures.append(texture)
        
        # атака
        self.attack_f_textures = self.attack_b_textures = self.idle_textures # заглушка
    
    def create_vampire_textures(self):
        """ Изменение внешнего вида на вампирский """
        
        # неподвижный режим
        self.idle_textures = []
        for i in range(4):
            texture = arcade.load_texture(f"resources/Hero/vampire/idle/{i}.png")
            self.idle_textures.append(texture)
        # ходьба вперед
        self.walk_f_textures = []
        for i in range(6):
            texture = arcade.load_texture(f"resources/Hero/vampire/walk_forward/{i}.png")
            self.walk_f_textures.append(texture)
        # ходьба назад
        self.walk_b_textures = []
        for i in range(6):
            texture = arcade.load_texture(f"resources/Hero/vampire/walk_back/{i}.png")
            self.walk_b_textures.append(texture)
        # получение урона
        self.hurt_textures = []
        for i in range(4):
            texture = arcade.load_texture(f"resources/Hero/vampire/hurt/{i}.png")
            self.hurt_textures.append(texture)
        
        self.death_textures = []
        for i in range(11):
            texture = arcade.load_texture(f"resources/Hero/vampire/death/{i}.png")
            self.death_textures.append(texture)
        
        self.attack_f_textures = []
        for i in range(12):
            texture = arcade.load_texture(f"resources/Hero/vampire/attack_forward/{i}.png")
            self.attack_f_textures.append(texture)
        
        self.attack_b_textures = []
        for i in range(12):
            texture = arcade.load_texture(f"resources/Hero/vampire/attack_back/{i}.png")
            self.attack_b_textures.append(texture)

    def update_animation(self, delta_time: float = 1/60):
        """ Обновление анимации """
        
        if self.dead: # смерть
            self.texture_change_time += delta_time
            if self.texture_change_time >= self.texture_change_delay:
                self.texture_change_time = 0
                self.current_texture += 1
                if self.current_texture >= len(self.death_textures):
                    self.disabled = True
                    self.current_texture = -1
                    ... # конец игры
                else:
                    self.texture = self.death_textures[self.current_texture]
        elif self.attack_f or self.attack_b: # если атакуем
            self.texture_change_time += delta_time
            if self.texture_change_time >= self.texture_change_delay:
                self.texture_change_time = 0
                self.current_texture += 1
            if self.attack_b: # атака назад
                if self.current_texture >= len(self.attack_b_textures):
                    self.attack_b= False
                    self.current_texture = 0
                else:
                    self.texture = self.attack_b_textures[self.current_texture]
            else: # в другом случае атакуем вперед
                if self.current_texture >= len(self.attack_f_textures):
                    self.attack_f = False
                    self.current_texture = 0
                else:
                    self.texture = self.attack_f_textures[self.current_texture]
        elif self.hurting:
            self.texture_change_time += delta_time
            if self.texture_change_time >= self.texture_change_delay:
                self.texture_change_time = 0
                self.current_texture += 1
                if self.current_texture >= len(self.hurt_textures):
                    self.hurting = False
                    self.current_texture = 0
                else:
                    self.texture = self.hurt_textures[self.current_texture]
        elif self.walk_f:
            self.texture_change_time += delta_time
            if self.texture_change_time >= self.texture_change_delay:
                self.texture_change_time = 0
                self.current_texture += 1
                self.current_texture %= len(self.walk_f_textures)
                self.texture = self.walk_f_textures[self.current_texture]
        elif self.walk_b:
            self.texture_change_time += delta_time
            if self.texture_change_time >= self.texture_change_delay:
                self.texture_change_time = 0
                self.current_texture += 1
                self.current_texture %= len(self.walk_b_textures)
                self.texture = self.walk_b_textures[self.current_texture]
        elif not self.dead:
            self.texture_change_time += delta_time
            if self.texture_change_time >= self.texture_change_delay:
                self.texture_change_time = 0
                self.current_texture += 1
                if self.current_texture >= len(self.idle_textures):
                    self.current_texture = 0
                self.texture = self.idle_textures[self.current_texture]
    
    def is_dead(self):
        return self.dead
    
    def walk_forward(self):
        """ Передвижение вперед """
        
        if not self.disabled:
            self.change_x = self.walk_speed
            self.walk_f = True
            self.walk_b = False
            
    def walk_back(self):
        """ Передвижение назад """
        
        if not self.disabled:
            self.change_x = -self.walk_speed
            self.walk_b = True
            self.walk_f = False
    
    def run_forward(self):
        """ Бег вперед """
        
        if not self.disabled:
            self.change_x = self.run_speed
    
    def run_back(self):
        """ Бег назад """
        
        if not self.disabled:
            self.change_x = -self.run_speed
    
    def jump(self):
        """ Прыжок персонажа """
        
        if self.bat and not self.disabled:
            self.change_y = self.walk_speed
        elif not self.disabled and self.change_y == 0:
            self.jumping = True
            self.change_y = self.jump_speed
    
    def down(self):
        """ Падение или спуск """
        
        if self.bat:
            self.change_y = -self.walk_speed
    
    def hurt(self, damage):
        """ Получение урона """
        
        if self.hurting:
            return
        self.hurting = True
        self.current_texture = -1
        self.jump()
        self.health -= damage
        if self.health <= 0:
            self.death()
        else:
            self.hurting = True
            self.walk_b = self.walk_f = False
    
    def death(self):
        """ Смерть """
        
        self.disabled = True
        self.dead = True

    def transform(self):
        """ Преврещение """
        
        if self.bat:
            self.bat = False
            self.create_vampire_textures()
            self.scale = 1.2
            self.texture_change_delay = 0.1  # секунд на кадр
        else:
            self.bat = True
            self.create_bat_textures()
            self.scale = 0.13
            self.texture_change_delay = 0.05  # секунд на кадр
    
    def attack(self,
               coords: tuple[int, int],
               speed: tuple[int, int],
               collision: list[arcade.SpriteList]) -> FireBoll:
        """ Атака """
        
        if not self.attack_b and not self.attack_f:
            if self.change_x >= 0:
                self.attack_f = True
                self.attack_b = False
            else:
                self.attack_b = True
                self.attack_f = False
        
        return FireBoll(
                    scale=0.05,
                    center_x=coords[0],
                    center_y=coords[1],
                    change_x=speed[0],
                    change_y=speed[1],
                    collision=collision
                )

    def update(self, delta_time):
        """ Перемещение персонажа """
        
        if self.change_x > 0:
            self.walk_f = True
            self.walk_b = False
        elif self.change_x < 0:
            self.walk_b = True
            self.walk_f = False
        else:
            self.walk_b = self.walk_f = False
        
        if self.change_y == 0:
            self.jumping = False
        
        self.update_animation(delta_time)
