from .bat_house import bat_house
from .estate import estate
from .skeleton_house import skeleton_house
from .werewolf_house import werewolf_house
from .library import library
from .sports_hall import sports_hall

"""
Словарь со всеми зданиями
"""

BUILDINGS = {
    "bat_house": bat_house,
    "estate": estate,
    "skeleton_house": skeleton_house,
    "werewolf_house": werewolf_house,
    "library": library,
    "sports_hall": sports_hall
}