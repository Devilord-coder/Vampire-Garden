import arcade
from src.settings import settings
from data.registry_data import database


class BaseWindow(arcade.Window):
    """Базовое окно для всех окон игры"""

    def __init__(self):
        super().__init__(settings.width, settings.height, settings.title,
                         resizable=settings.resizable, fullscreen=settings.fullscreen)
        self.set_minimum_size(settings.width_min, settings.height_min)
        # self.center_window() - не работает (по крайней мере на Маке)
        self.background_color = arcade.color.BLACK
        self.sprites = arcade.SpriteList()
        self.set_mouse_visible(False)
        self.mouse = arcade.Sprite('resources/Cursor.png', scale=2)
        self.mouse.center_x = self.width // 2
        self.mouse.center_y = self.height // 2
        self.sprites.append(self.mouse)

        # Храним представления
        self.views = {}
        
        # База данных
        self.db = database
    
    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse.center_x = x
        self.mouse.center_y = y

    def get_view(self, view_name):
        """ Получить или создать представление по имени """

        if view_name not in self.views:
            if view_name == "start": # начальное окно - авторизация
                from src.windows.start_view import StartView
                self.views[view_name] = StartView(self)
            elif view_name == "registration": # окно регистрации
                from src.windows.registration_view import RegistrationView
                self.views[view_name] = RegistrationView(self)
            elif view_name == "main_menu": # главное окно
                from src.windows.main_menu_view import MainMenuView
                self.views[view_name] = MainMenuView(self)
            elif view_name == "prehistory": # окно предыстории
                from src.windows.prehistory_view import PrehistoryView
                self.views[view_name] = PrehistoryView(self)
            elif view_name == "main_game": # главное окно игры
                from src.windows.game.main_game_view import MainGameView
                self.views[view_name] = MainGameView(self)

        return self.views[view_name]
    
    def on_draw(self):
        
        self.sprites.draw()
        return super().on_draw()
    
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
        # выйти при нажатии COMMAND + Q или CTRL + Q
        if key == arcade.key.Q and modifiers in {arcade.key.MOD_COMMAND, arcade.key.MOD_CTRL}:
            self.close()
    
    def close(self):
        """ Закрытие окна """
        
        # Перед закрытием отключаемя от БД
        self.db.close()
        return super().close()
