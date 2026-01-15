import arcade
from arcade.gui import (UIManager, UIAnchorLayout, UIBoxLayout,
                        UIFlatButton, UILabel)
from src.styles import *
from random import choice
from os import listdir


class PortalView(arcade.View):
    """ Представление внутри портала """
    
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.background = arcade.load_texture("resources/Battlegrounds/Terrace/terrace.png")

    def setup(self):
        """ Инициализация представления """
        
        # UIManager — сердце GUI
        self.manager = UIManager()
        self.manager.enable()  # Включить, чтоб виджеты работали
        
        # Layout для организации — как полки в шкафу
        self.anchor_layout = UIAnchorLayout()  # Центрирует виджеты
        self.box_layout = UIBoxLayout(vertical=True, space_between=20)  # Вертикальный стек
        
        choose_text = UILabel(
            text="ВЫБЕРИТЕ УРОВЕНЬ СЛОЖНОСТИ",
            font_size=18,
            multiline=True,
            text_color=arcade.color.WHITE
        )
        
        easy_btn = UIFlatButton(
            text="EASY",
            width=200,
            style=EASY_STYLE
        )
        @easy_btn.event("on_click")
        def on_click_settings(event):
            self.start_game("easy")
        
        medium_btn = UIFlatButton(
            text="MEDIUM",
            width=200,
            style=MEDIUM_STYLE
        )
        @medium_btn.event("on_click")
        def on_click_settings(event):
            self.start_game("medium")
        
        hard_btn = UIFlatButton(
            text="HARD",
            width=200,
            style=HARD_STYLE
        )
        @hard_btn.event("on_click")
        def on_click_settings(event):
            self.start_game("hard")
        
        # ==== ДОБАВЛЯЕМ ВИДЖЕТЫ ПО ПОРЯДКУ ====
        self.box_layout.add(choose_text)
        self.box_layout.add(easy_btn)
        self.box_layout.add(medium_btn)
        self.box_layout.add(hard_btn)
        
        self.anchor_layout.add(self.box_layout)  # Box в anchor
        self.manager.add(self.anchor_layout)  # Всё в manager

    def on_show_view(self):
        """ Вызывается при показе этого представления """
        
        self.setup()

    def on_draw(self):
        """ Метод загрузки текста, картинки и кнопки """
        
        self.clear()
        
        # ------------- ЗАДНИЙ ФОН -------------
        arcade.draw_texture_rect(self.background, arcade.rect.XYWH(
            self.width // 2, self.height // 2,
            self.width, self.height
        ))
        
        self.manager.draw()

    def on_resize(self, width: float, height: float):
        """ Метод отработки изменения окна """
        super().on_resize(width, height)
    
    def on_key_press(self, key, modifiers):
        """ Нажатие клавиш """
        
        if key == arcade.key.ESCAPE:
            self.manager.disable()
            self.window.switch_view("main_map")
    
    def start_game(self, degree: str):
        """ Начало игры

        Args:
            degree (str): "easy", "medium" или "hard" - степень сложности игры
        """
        
        self.manager.disable()
        self.window.get_view("battle")
        self.window.views["battle"].set_map(f"{degree}/{choice(list(filter(lambda x: x[-4:] == ".tmx",
                                            listdir(f"maps/{degree}"))))}")
        self.window.switch_view("battle")