import arcade
import sqlite3
from src.settings import settings
from data import RegistryDataBase, GameData
from src.registry import reg

from src.windows.game.main_map_view import MainMapView
from src.windows.shop_view import ShopView
from src.windows.prehistory_view import PrehistoryView
from src.windows.game.garden import GardenView
from src.windows.game.buildings.library import Library
from src.windows.game.buildings.bat_house import BatHouse
from src.windows.game.buildings.skeleton_house import SkeletonHouse
from src.windows.game.buildings.werewolf_house import WerewolfHouse
from src.windows.choose_game_view import ChooseGameView
from src.windows.game.battle import BattleStatisticView
from src.windows.main_menu_view import MainMenuView
from src.windows.game.main_game_view import MainGameView
from src.windows.registration_view import RegistrationView
from src.windows.start_view import StartView
from src.windows.game.portal_view import PortalView
from src.windows.game.battle import BattleView
from src.windows.tutorial_view import TutorialView
from src.windows.final import Final
from src.windows.game.battle import BattleWinView


class BaseWindow(arcade.Window):
    """Базовое окно для всех окон игры"""

    def __init__(self):
        super().__init__(
            settings.width,
            settings.height,
            settings.title,
            resizable=settings.resizable,
            fullscreen=settings.fullscreen,
        )
        self.set_minimum_size(settings.width_min, settings.height_min)
        # self.center_window() - не работает (по крайней мере на Маке)

    def setup(self):
        self.background_color = arcade.color.BLACK
        self.sprites = arcade.SpriteList()
        self.set_mouse_visible(False)
        self.mouse = arcade.Sprite("resources/Cursor.png", scale=2)
        self.mouse.center_x = self.width // 2
        self.mouse.center_y = self.height // 2
        self.mouse.visible = True
        self.sprites.append(self.mouse)

        # Храним представления
        self.views = {}

        # База данных
        self.con = sqlite3.connect("vampire_garden_db.db")
        self.reg_db = RegistryDataBase(self.con)

        self.bg_sound = reg.background_sound

        self.game_number = 0
        self.login = None
        self.game_id = None  # Индекс игры
        self.garden_id = None  # Индекс огорода
        self.quantity_money = None  # Количество денег

        self.bg_sound_playback = arcade.play_sound(self.bg_sound, loop=True)

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse.center_x = x
        self.mouse.center_y = y

    def get_view(self, view_name):
        """Получить или создать представление по имени"""

        if view_name not in self.views:
            if view_name == "start":  # начальное окно - авторизация
                self.views[view_name] = StartView(self)
            elif view_name == "registration":  # окно регистрации
                self.views[view_name] = RegistrationView(self)
            elif view_name == "main_menu":  # главное окно
                self.views[view_name] = MainMenuView(self)
            elif view_name == "prehistory":  # окно предыстории
                self.views[view_name] = PrehistoryView(self)
            elif view_name == "main_game":  # главное окно игры
                self.views[view_name] = MainGameView(self)
            elif view_name == "main_map":  # основная карта
                self.views[view_name] = MainMapView(self)
            elif view_name == "shop":  # представление магазина
                self.views[view_name] = ShopView(self)
            elif view_name == "choose_game":
                self.views[view_name] = ChooseGameView(self)
            elif view_name in {"game_1", "game_2", "game_3"}:
                if view_name == "game_1":
                    self.game_number = 1
                elif view_name == "game_2":
                    self.game_number = 2
                elif view_name == "game_3":
                    self.game_number = 3

                game_data = GameData(self)
                result = game_data.get_game_state()
                if result:
                    self.views[view_name] = MainMapView(self)
                else:
                    self.views[view_name] = PrehistoryView(self)
            elif view_name == "garden":  # Представление огорода
                self.views[view_name] = GardenView(self)
            elif view_name == "settings":
                ...
            elif view_name == "library":  # Представление библиотеки с информацией игры
                self.views[view_name] = Library(self)
            elif view_name == "bat_house":  # Представление дома летучих мышей
                self.views[view_name] = BatHouse(self)
            elif view_name == "sceleton_house":  # Представление дома скелетов
                self.views[view_name] = SkeletonHouse(self)
            elif view_name == "werewolf_house":  # Представление дома оборотней
                self.views[view_name] = WerewolfHouse(self)
            elif view_name == "portal":  # представление портала
                self.views[view_name] = PortalView(self)
            elif view_name == "battle":  # битва
                self.views[view_name] = BattleView(self)
            elif view_name == "battle_statistic":  # итоги сражения
                self.views[view_name] = BattleStatisticView(self)
            elif view_name == "tutorial":  # Туториал
                self.views[view_name] = TutorialView(self)
            elif view_name == "final":  # Финальное окно
                self.views[view_name] = Final(self)
            elif view_name == "win_battle_view":
                self.views[view_name] = BattleWinView(self)

        return self.views[view_name]

    def on_draw(self):

        self.sprites.draw()
        return super().on_draw()

    def on_update(self, delta_time):
        """Обновление логики"""

        if self.mouse.visible and self.mouse not in self.sprites:
            self.sprites.append(self.mouse)
        elif not self.mouse.visible and self.mouse in self.sprites:
            self.sprites.pop(self.sprites.index(self.mouse))

    def get_parts(self) -> tuple[int, int, int, int]:
        """Функция для разделения экрана на равные части

        Returns:
            tuple[int, int, int, int]: одна сотая часть экрана по х и у,
        а также центры окна по х и у
        """

        # part_x и part_y - одна сотая часть экрана по х и у,
        # так будет легче ставить кнопки на разных размерах экрана
        part_x = self.width // 100
        part_y = self.height // 100
        center_x = part_x * 50
        center_y = part_y * 50

        return (part_x, part_y, center_x, center_y)

    def switch_view(self, view_name):
        """Переключиться на представление"""
        view = self.get_view(view_name)
        self.show_view(view)

    def on_key_press(self, key, modifiers):
        """Нажатие клавиши"""

        # выйти при нажатии COMMAND + Q или CTRL + Q
        if key == arcade.key.Q and modifiers in {
            arcade.key.MOD_COMMAND,
            arcade.key.MOD_CTRL,
        }:
            self.close()

    def close(self):
        """Закрытие окна"""

        # Перед закрытием отключаемя от БД
        self.reg_db.close()
        self.con.close()
        return super().close()
