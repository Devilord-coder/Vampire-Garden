import arcade
from arcade.gui import UIManager, UILabel, UITextureButton
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout

from data.statistic_data import StatisticData
from src.auxiliary_classes.scale import scale
from src.settings import settings
from src.registry import reg

EXIT_SCALE = scale(120, settings.height)


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
        self.exit_texture = arcade.load_texture("resources/buttons/exit/shop_exit.png")

        self.door_sound = reg.door_sound

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

        self.game_statistic = StatisticData(self.window)
        self.creat_text()
        self.exit_button_init()

    def creat_text(self):
        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=20)
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
            if index > len(self.texts) - 1:
                # Если текст закончился, выходим
                break
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

        rect = arcade.rect.XYWH(self.width // 2, self.height // 2, 700, 700)
        arcade.draw_texture_rect(self.paper_texture, rect)

        self.manager.draw()

    def exit_button_init(self):
        """Инициализация кнопки для перехода на представление главной карты"""
        x = 10 + self.exit_texture.width // 2 * EXIT_SCALE
        y = self.height - (self.exit_texture.height * EXIT_SCALE) - 10
        button = UITextureButton(
            center_x=x,
            y=y,
            texture=self.exit_texture,
            texture_hovered=self.exit_texture,
            texture_pressed=self.exit_texture,
            scale=EXIT_SCALE,
        )

        @button.event("on_click")
        def on_click(event):
            arcade.play_sound(self.door_sound, 1, loop=False)
            self.window.switch_view("main_map")

        self.manager.add(button)

    def on_show_view(self):
        """Активация ui менеджера"""
        if self.manager:
            self.manager.enable()
        if self.game_statistic:
            self.box_layout.clear()
            self.anchor_layout.clear()
            self.game_statistic.update()
            self.creat_text()

    def on_hide_view(self):
        """Выключение ui менеджера"""
        if self.manager:
            self.manager.disable()
