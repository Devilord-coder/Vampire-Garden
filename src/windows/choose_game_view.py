import arcade
from src.styles import *
from src.registry import reg
from arcade.gui import UIManager, UIFlatButton, UILabel
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout


class ChooseGameView(arcade.View):
    """Окно для выбора сохранения в игре"""

    def __init__(self, window):
        super().__init__()
        self.window = window  # Ссылка на главное окно
        self.background = arcade.load_texture(
            "resources/Background/start_background.jpeg"
        )
        
        self.setup()
    
    def setup(self):
        
        # UIManager — сердце GUI
        self.manager = UIManager()
        self.manager.enable()  # Включить, чтоб виджеты работали

        # Layout для организации — как полки в шкафу
        self.anchor_layout = UIAnchorLayout()  # Центрирует виджеты
        self.box_layout = UIBoxLayout(
            vertical=True, space_between=20
        )  # Вертикальный стек

        choose_game_text = UILabel(
            text="ВЫБЕРИТЕ СОХРАНЕНИЕ",
            font_size=20,
            text_color=TEXT_COLOR,
            multiline=True,
        )

        # кнопка для открытия 1 ячейки для сохранения игры
        game_1_btn = UIFlatButton(text="ИГРА 1", style=button_style, width=200)

        @game_1_btn.event("on_click")
        def on_click_settings(event):
            self.manager.disable()
            self.window.switch_view("game_1")
            arcade.play_sound(reg.button_click_sound)
        
        # кнопка для открытия 2 ячейки для сохранения игры
        game_2_btn = UIFlatButton(text="ИГРА 2", style=button_style, width=200)

        @game_2_btn.event("on_click")
        def on_click_settings(event):
            self.manager.disable()
            self.window.switch_view("game_2")
            arcade.play_sound(reg.button_click_sound)
        # кнопка для открытия 3 ячейки для сохранения игры
        game_3_btn = UIFlatButton(text="ИГРА 3", style=button_style, width=200)

        @game_3_btn.event("on_click")
        def on_click_settings(event):
            self.manager.disable()
            self.window.switch_view("game_3")
            arcade.play_sound(reg.button_click_sound)

        # ==== ДОБАВЛЯЕМ ВИДЖЕТЫ ПО ПОРЯДКУ ====
        self.box_layout.add(choose_game_text)
        self.box_layout.add(game_1_btn)
        self.box_layout.add(game_2_btn)
        self.box_layout.add(game_3_btn)

        self.anchor_layout.add(self.box_layout)  # Box в anchor
        self.manager.add(self.anchor_layout)  # Всё в manager

    def on_show_view(self):
        """Вызывается при показе этого представления"""
        
        self.setup()

    def on_draw(self):
        """Рисование"""
        self.clear()

        # ----- ЗАДНИЙ ФОН -----
        arcade.draw_texture_rect(
            self.background,
            arcade.rect.XYWH(
                self.width // 2, self.height // 2, self.width, self.height
            ),
        )

        self.manager.draw()

    def on_update(self, delta_time):
        """Обновление логики"""

        ...

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.switch_view("start")

    def on_show_view(self):
        """Активация ui менеджера"""
        if self.manager:
            self.manager.enable()

    def on_hide_view(self):
        """Выключение ui менеджера"""
        if self.manager:
            self.manager.disable()
