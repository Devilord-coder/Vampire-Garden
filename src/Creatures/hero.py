import arcade


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
        
        # идет вперед
        self.walk_f = False
        # идет назад
        self.walk_b = False
        self.hurting = False
        self.dead = False
        self.bat = False
        
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
        
        self.death_textures = []
        for i in range(18):
            texture = arcade.load_texture(f"resources/Hero/bat/death/{i}.png")
            self.death_textures.append(texture)
    
    def create_vampire_textures(self):
        """ изменение внешнего вида на вампирский """
        
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
        self.hurt_textures = self.idle_textures # заглушка
        
        self.death_textures = []
        for i in range(11):
            texture = arcade.load_texture(f"resources/Hero/vampire/death/{i}.png")
            self.death_textures.append(texture)

    def update_animation(self, delta_time: float = 1/60):
        """ Обновление анимации """
        
        if self.dead:
            self.texture_change_time += delta_time
            if self.texture_change_time >= self.texture_change_delay:
                self.texture_change_time = 0
                self.current_texture += 1
                if self.current_texture >= len(self.death_textures):
                    self.disabled = True
                    ... # конец игры
                else:
                    self.texture = self.death_textures[self.current_texture]
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
        else:
            self.texture_change_time += delta_time
            if self.texture_change_time >= self.texture_change_delay:
                self.texture_change_time = 0
                self.current_texture += 1
                if self.current_texture >= len(self.idle_textures):
                    self.current_texture = 0
                self.texture = self.idle_textures[self.current_texture]
    
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
        """ Беш вперед """
        
        if not self.disabled:
            self.change_x = self.run_speed
    
    def run_back(self):
        """ Бег назад """
        
        if not self.disabled:
            self.change_x = -self.run_speed
    
    def jump(self):
        """ Прыжок персонажа """
        
        if self.bat:
            self.change_y = self.walk_speed
        elif not self.disabled and self.change_y == 0:
            self.change_y = self.jump_speed
    
    def down(self):
        if self.bat:
            self.change_y = -self.walk_speed
    
    def hurt(self, damage):
        """ Получение урона """
        
        self.health -= damage
        if self.health <= 0:
            self.death()
        else:
            self.hurting = True
            self.walk_b = self.walk_f = False
    
    def death(self):
        self.disabled = True
        self.dead = True

    def transform(self):
        if self.bat:
            self.bat = False
            self.create_vampire_textures()
            self.scale = 1.2
        else:
            self.bat = True
            self.create_bat_textures()
            self.scale = 0.2

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
        
        self.update_animation()
