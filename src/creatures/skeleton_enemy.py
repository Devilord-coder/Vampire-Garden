from .enemy import Enemy


class SkeletonEnemy(Enemy):
    """ Класс скелета """
    
    def __init__(self, enemies_name_list: list = [], scaling = 1, health = 100, folder_name = "skeleton", walk_speed = 0, fly_jump_speed = 0, power = 25):
        super().__init__(enemies_name_list, scaling, health, folder_name, walk_speed, fly_jump_speed, power)