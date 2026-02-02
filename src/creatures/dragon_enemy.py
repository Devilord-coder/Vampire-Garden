from .enemy import Enemy


class DragonEnemy(Enemy):
    def __init__(self, enemies_name_list: list = [], scaling = 1, health = 500, folder_name = "dragon", walk_speed = 5, fly_jump_speed = 0, power = 100):
        super().__init__(enemies_name_list, scaling, health, folder_name, walk_speed, fly_jump_speed, power)