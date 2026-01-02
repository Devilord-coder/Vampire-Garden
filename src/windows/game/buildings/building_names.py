from .bat_house import BatHouse

# from .estate import estate
from .skeleton_house import SkeletonHouse
from .werewolf_house import WerewolfHouse
from .library import Library

# from .sports_hall import sports_hall

"""
Словарь со всеми зданиями
"""

BUILDINGS = {
    "bat_house": BatHouse,
    # "estate": estate,
    "skeleton_house": SkeletonHouse,
    "werewolf_house": WerewolfHouse,
    "library": Library,
    # "sports_hall": sports_hall,
}
