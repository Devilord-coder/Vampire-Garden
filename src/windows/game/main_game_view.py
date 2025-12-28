import arcade
from src.settings import settings
from arcade.gui import UIManager
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout


class MainGameView(arcade.View):
    """Главное меню игры"""

    def __init__(self, window):
        super().__init__()
        self.window = window  # Ссылка на главное окно
        self.background = arcade.load_texture('resources/Background/start_background.jpeg')
        self.shape_list = arcade.shape_list.ShapeElementList()
        
        # UIManager — сердце GUI
        self.manager = UIManager()
        self.manager.enable()  # Включить, чтоб виджеты работали
        
        # Layout для организации — как полки в шкафу
        self.anchor_layout = UIAnchorLayout()  # Центрирует виджеты
        self.box_layout = UIBoxLayout(vertical=True, space_between=20)  # Вертикальный стек
        
        ...
        
        # ==== ДОБАВЛЯЕМ ВИДЖЕТЫ ПО ПОРЯДКУ ====
        ...
        
        self.anchor_layout.add(self.box_layout)  # Box в anchor
        self.manager.add(self.anchor_layout)  # Всё в manager

    def on_show_view(self):
        """Вызывается при показе этого представления"""
        
        ...

    def on_draw(self):
        """Рисование"""
        self.clear()
        
        # ----- ЗАДНИЙ ФОН -----
        arcade.draw_texture_rect(self.background, arcade.rect.XYWH(
            self.width // 2, self.height // 2,
            self.width, self.height
        ))
        
        self.shape_list.draw()
        self.manager.draw()

    def on_update(self, delta_time):
        """Обновление логики"""
        
        ...

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.switch_view("start")
