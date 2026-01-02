import arcade


class Enemy(arcade.Sprite):
    def __init__(
        self, scaling: float = 1, health: int = 100,
        folder_name: str = "skeleton", walk_speed: int = 0,
        fly_jump_speed: int = 0
    ):
        super().__init__()
        
        self.scale = scaling
        self.health = health
        
        self.change_x = walk_speed
        self.change_y = fly_jump_speed
        
        self.textures_init()
    
    def textures_init(self):
        ...
        
    def update(self, delta_time):
        ...
        
    def update_animation(self, delta_time):
        ...
        self.update_animation(delta_time)