import arcade
from src.settings import settings
from data.registry_data import registry_database
from src.registry import reg


class BaseWindow(arcade.Window):
    """ Базовое окно для всех окон игры """

    def __init__(self):
        super().__init__(settings.width, settings.height, settings.title,
                         resizable=settings.resizable, fullscreen=settings.fullscreen)
        self.set_minimum_size(settings.width_min, settings.height_min)
        # self.center_window() - не работает (по крайней мере на Маке)
    
    def setup(self):
        self.background_color = arcade.color.BLACK
        self.sprites = arcade.SpriteList()
        self.set_mouse_visible(False)
        self.mouse = arcade.Sprite('resources/Cursor.png', scale=2)
        self.mouse.center_x = self.width // 2
        self.mouse.center_y = self.height // 2
        self.mouse.visible = True
        self.sprites.append(self.mouse)

        # Храним представления
        self.views = {}
        
        # База данных
        self.reg_db = registry_database
        
        self.bg_sound = reg.background_sound
        self.bg_sound_playback = arcade.play_sound(self.bg_sound)
    
    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse.center_x = x
        self.mouse.center_y = y

    def get_view(self, view_name):
        """ Получить или создать представление по имени """

        if view_name not in self.views:
            if view_name == "start":  # начальное окно - авторизация
                from src.windows.start_view import StartView
                self.views[view_name] = StartView(self)
            elif view_name == "registration":  # окно регистрации
                from src.windows.registration_view import RegistrationView
                self.views[view_name] = RegistrationView(self)
            elif view_name == "main_menu":  # главное окно
                from src.windows.main_menu_view import MainMenuView
                self.views[view_name] = MainMenuView(self)
            elif view_name == "prehistory":  # окно предыстории
                from src.windows.prehistory_view import PrehistoryView
                self.views[view_name] = PrehistoryView(self)
            elif view_name == "main_game": # главное окно игры
                from src.windows.game.main_game_view import MainGameView
                self.views[view_name] = MainGameView(self)
            elif view_name == 'main_map':  # основная карта
                from src.windows.game.main_map_view import MainMapView
                self.views[view_name] = MainMapView(self)
            elif view_name == 'shop':  # пркдставление магазина
                from src.windows.shop_view import ShopView
                self.views[view_name] = ShopView(self)
            elif view_name == "choose_game":
                from src.windows.choose_game_view import ChooseGameView
                self.views[view_name] = ChooseGameView(self)
            elif view_name == "game_1":
                ... # Заглушка - пока просто открывается главное окно игры
                from src.windows.prehistory_view import PrehistoryView
                self.views[view_name] = PrehistoryView(self)
            elif view_name == "game_2":
                ... # Заглушка - пока просто открывается главное окно игры
                from src.windows.prehistory_view import PrehistoryView
                self.views[view_name] = PrehistoryView(self)
            elif view_name == "game_3":
                ... # Заглушка - пока просто открывается главное окно игры
                from src.windows.prehistory_view import PrehistoryView
                self.views[view_name] = PrehistoryView(self)
            elif view_name == "portal":
                from src.windows.game.portal_view import PortalView
                self.views[view_name] = PortalView(self)
            elif view_name == "battle":
                from src.windows.game.battle import BattleView
                self.views[view_name] = BattleView(self)
            elif view_name == "battle_statistic":
                from src.windows.game.battle import BattleStatisticView
                self.views[view_name] = BattleStatisticView(self)
            elif view_name == "settings":
                ...

        return self.views[view_name]
    
    def on_draw(self):
        
        self.sprites.draw()
        return super().on_draw()
    
    def on_update(self, delta_time):
        if self.mouse.visible and self.mouse not in self.sprites:
            self.sprites.append(self.mouse)
        elif not self.mouse.visible and self.mouse in self.sprites:
            self.sprites.pop(self.sprites.index(self.mouse))
    
    def get_parts(self) -> tuple[int, int, int, int]:
        """ Функция для разделения экрана на равные части

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
        """ Переключиться на представление """

        view = self.get_view(view_name)
        self.show_view(view)

    def on_key_press(self, key, modifiers):
        """ Нажатие клавиши """
        
        # выйти при нажатии COMMAND + Q или CTRL + Q
        if key == arcade.key.Q and modifiers in {arcade.key.MOD_COMMAND, arcade.key.MOD_CTRL}:
            self.close()
    
    def close(self):
        """ Закрытие окна """
        
        # Перед закрытием отключаемя от БД
        self.reg_db.close()
        return super().close()
