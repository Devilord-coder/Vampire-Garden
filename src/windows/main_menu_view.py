import arcade
from pyglet.graphics import Batch
from src.settings import settings
from arcade.gui import UIManager, UITextureButton, UILabel, UIFlatButton
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout
from src.styles import *


class MainMenuView(arcade.View):
    """Главное меню игры"""

    def __init__(self, window):
        super().__init__()
        self.window = window  # Ссылка на главное окно
        self.background = arcade.load_texture('resources/Background/start_background.jpeg')
        self.batch = Batch()
        self.shape_list = arcade.shape_list.ShapeElementList()
        self.name_game = None
        self.rect_outline = None
        
        # UIManager — сердце GUI
        self.manager = UIManager()
        self.manager.enable()  # Включить, чтоб виджеты работали
        
        # Layout для организации — как полки в шкафу
        self.anchor_layout = UIAnchorLayout()  # Центрирует виджеты
        self.box_layout = UIBoxLayout(vertical=True, space_between=20)  # Вертикальный стек

        part_x, part_y, center_x, center_y = self.window.get_parts()
        
        # надпись "ГЛАВНОЕ МЕНЮ"
        mainmenu_text = UILabel(
            text="ГЛАВНОЕ МЕНЮ",
            text_color=TEXT_COLOR,
            font_size=30,
            multiline=True
        )
        
        # кнопка для начатия игры красивая - не подходит по стилю
        # texture_normal = arcade.load_texture("resources/buttons/PLAY/PLAY_Default.png")
        # texture_hovered = arcade.load_texture("resources/buttons/PLAY/PLAY_Hovered.png")
        # texture_pressed = arcade.load_texture("resources/buttons/PLAY/PLAY_Hovered.png")
        # play_btn = UITextureButton(texture=texture_normal, 
        #                                 texture_hovered=texture_hovered,
        #                                 texture_pressed=texture_pressed,
        #                                 scale=1.0)
        # кнопка для начатия игры
        play_btn = UIFlatButton(
            text="ИГРАТЬ",
            style=button_style,
            width=200
        )
        @play_btn.event("on_click")
        def on_click_settings(event):
            self.window.switch_view("main_map")
        
        settings_btn = UIFlatButton(
            text="НАСТРОЙКИ",
            style=button_style,
            width=200
        )
        @settings_btn.event("on_click")
        def on_click_settings(event):
            self.window.switch_view("settings")
        
        escape_btn = UIFlatButton(
            text='ВЫХОД',
            style=button_style,
            width=200
        )
        @escape_btn.event("on_click")
        def on_click_settings(event):
            self.window.switch_view("start")
        
        # ==== ДОБАВЛЯЕМ ВИДЖЕТЫ ПО ПОРЯДКУ ====
        self.box_layout.add(mainmenu_text)
        self.box_layout.add(play_btn)
        self.box_layout.add(settings_btn)
        self.box_layout.add(escape_btn)
        
        self.anchor_layout.add(self.box_layout)  # Box в anchor
        self.manager.add(self.anchor_layout)  # Всё в manager

    def on_show_view(self):
        """ Вызывается при показе этого представления """
        self.create_text()

    def on_draw(self):
        """Рисование"""
        self.clear()
        
        # ----- ЗАДНИЙ ФОН -----
        arcade.draw_texture_rect(self.background, arcade.rect.XYWH(
            self.width // 2, self.height // 2,
            self.width, self.height
        ))
        
        self.manager.draw()

    def on_update(self, delta_time):
        """Обновление логики"""
        pass

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.switch_view("start")
