import arcade
from pyglet.graphics import Batch
from src.settings import settings
from arcade.gui import UIManager, UITextureButton, UILabel
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

        part_x, part_y, center_x, center_y = self.window.get_parts()
        
        ...
        
        # Добавляем все виджеты
        ...
        
        self.anchor_layout.add(self.box_layout)  # Box в anchor
        self.manager.add(self.anchor_layout)  # Всё в manager

    def on_show_view(self):
        """Вызывается при показе этого представления"""
        
        ...

    def on_draw(self):
        """Рисование"""
        self.clear()
        
        # рисуем задний фон
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

    def on_resize(self, width: float, height: float):
        """Обработка изменения размера окна"""
        super().on_resize(width, height)
        self.create_text()

    def create_text(self):
        """Создание текста и рамки для главного меню"""
        # Очищаем предыдущие объекты
        self.batch = Batch()
        if self.shape_list:
            self.shape_list.clear()

        center_x = self.window.width // 2
        center_y = self.window.height // 1.2

        # Расчет размера шрифта
        base_width = settings.width_min
        font_size = int(24 * (self.window.width / base_width))

        # Создаем текст
        self.name_game = arcade.Text(
            "Главное меню",
            center_x,
            center_y,
            arcade.color.RED,
            font_size,
            bold=True,
            align="center",
            anchor_x="center",
            anchor_y="center",
            batch=self.batch,
        )

        # Создаем рамку
        text_width = self.name_game.content_width
        text_height = self.name_game.content_height
        padding = int(min(self.window.width, self.window.height) * 0.05)
        rect_width = text_width + padding
        rect_height = text_height + padding

        self.rect_outline = arcade.shape_list.create_rectangle_outline(
            center_x=center_x,
            center_y=center_y,
            width=rect_width,
            height=rect_height,
            color=arcade.color.RED,
            border_width=2
        )
        self.shape_list.append(self.rect_outline)
