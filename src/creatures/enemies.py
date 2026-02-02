from .skeleton_enemy import SkeletonEnemy
from .demon_enemy import DemonEnemy
from .dragon_enemy import DragonEnemy


ENEMIES = {
    "skeleton": SkeletonEnemy,
    "demon": DemonEnemy,
    "dragon": DragonEnemy
}

ENEMIES_PRICE = {
    "skeleton": 25,
    "demon": 50,
    "dragon": 100
}