import arcade

MONEY_TYPES = ["gold", "silver", "bronze"]


class Money(arcade.Sprite):
    def __init__(
        self, path_or_texture = None, type="bronze",
        scale = 1, center_x = 0, center_y = 0, angle = 0,
        **kwargs
        ):
        super().__init__(
            path_or_texture, scale, center_x, center_y, angle, **kwargs
            )
        self.scale = 0.2
        if type in MONEY_TYPES:
            self.type = type
        else:
            self.type = MONEY_TYPES[2]
        self.textures = []
        for i in range(4):
            texture = arcade.load_texture(f"resources/Objects/money/{self.type}/{i}.png")
            self.textures.append(texture)
        
        self.texture = self.textures[0]
        self.current_texture = 0
        self.texture_change_time = 0
        self.texture_change_delay = 0.3  # секунд на кадр
    
    def update_animation(self, delta_time):
        """ Обновление анимации """
        
        self.texture_change_time += delta_time
        if self.texture_change_time >= self.texture_change_delay:
            self.texture_change_time = 0
            self.current_texture += 1
            if self.current_texture >= len(self.textures):
                self.current_texture = 0
            self.texture = self.textures[self.current_texture]
    
    def update(self, delta_time):
        self.update_animation(delta_time)