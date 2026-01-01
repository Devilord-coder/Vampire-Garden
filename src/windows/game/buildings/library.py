import arcade
from arcade.gui import UIManager, UILabel
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout

# from src.windows.game.buildings.building import Building
from data.statistic_data import StatisticData


class Library(arcade.View):
    """Здание библиотеки"""

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.name = "library"
        self.background_texture = arcade.load_texture(
            "resources/Background/library.jpg"
        )
        self.paper_texture = arcade.load_texture("resources/Background/paper.png")
        self.manager = None
        self.text_color = arcade.color.CORDOVAN
        self.texts = [
            "Ваши сбережения составляют:",
            "Количество семян мандрагоры:",
            "Количество семян белладонны:",
            "Количество семян красной розы:",
            "Выращено мандрагоры:",
            "Выращено белладонны:",
            "Выращено красной розы:",
            "Воинов летучих мышей:",
            "Воинов скелетов:",
            "Воинов оборотней:",
        ]
        self.setup()

    def setup(self):
        """Настройка текста статистики из бд"""
        self.manager = UIManager()
        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=20)

        self.game_statistic = StatisticData(self.window)
        line = self.game_statistic.name
        label = UILabel(
            text=f"Здравствуйте, {line}!",
            font_size=34,
            width=800,
            align="center",
            text_color=self.text_color,
        )
        self.box_layout.add(label)

        for index, line in enumerate(self.game_statistic.game_information):
            new_line = f"{self.texts[index]} {line}"
            label = UILabel(
                text=new_line,
                font_size=25,
                width=800,
                text_color=self.text_color,
            )
            self.box_layout.add(label)

        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)

    def on_draw(self):
        self.clear()
        rect = arcade.rect.XYWH(
            self.width // 2, self.height // 2, self.width, self.height
        )
        arcade.draw_texture_rect(self.background_texture, rect)

        rect = arcade.rect.XYWH(self.width // 2, self.height // 2, 1350, 700)
        arcade.draw_texture_rect(self.paper_texture, rect)

        self.manager.draw()

    def on_show_view(self):
        """Активация ui менеджера"""
        if self.manager:
            self.manager.enable()

    def on_hide_view(self):
        """Выключение ui менеджера"""
        if self.manager:
            self.manager.disable()
