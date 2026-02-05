from .enemy import Enemy


class DemonEnemy(Enemy):
    def __init__(self, enemies_name_list: list = [], scaling = 0.4, health = 250, folder_name = "demon", walk_speed = 3, fly_jump_speed = 0, power = 50):
        super().__init__(enemies_name_list, scaling, health, folder_name, walk_speed, fly_jump_speed, power)