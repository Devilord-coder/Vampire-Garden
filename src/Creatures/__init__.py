from .hero import Hero
from .enemies import ENEMIES, ENEMIES_PRICE
from .garden_minion import GardenMinion
from .rabbit import Rabbit

"""
Модуль с персонажами для боя
"""

PACKAGE_VERSION = "1.0.0"

__all__ = [
    "Hero",
    "ENEMIES",
    "GardenMinion",
    "Rabbit",
    "ENEMIES_PRICE"
]