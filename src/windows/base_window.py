# base_window.py
import arcade
from src.settings import settings


class BaseWindow(arcade.Window):
    """Базовое окно для всех окон игры"""

    def __init__(self):
        super().__init__(settings.width, settings.height, settings.title,
                         resizable=settings.resizable, fullscreen=settings.fullscreen)
        self.set_minimum_size(settings.width_min, settings.height_min)
        self.center_window()
        self.background_color = arcade.color.BLACK

        # Храним представления
        self.views = {}

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
                ...

        return self.views[view_name]

    def switch_view(self, view_name):
        """ Переключиться на представление """

        view = self.get_view(view_name)
        self.show_view(view)

    def on_key_press(self, key, modifiers):
        # выйти при нажатии COMMAND + Q или CTRL + Q
        if key == arcade.key.Q and modifiers in {arcade.key.MOD_COMMAND, arcade.key.MOD_CTRL}:
            self.close()
