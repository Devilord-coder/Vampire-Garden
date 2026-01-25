import arcade
from arcade.gui import UIManager, UILabel
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout

from data.statistic_data import StatisticData

FRAME_DURATION = 0.05  # Время показа каждого кадра


class Final(arcade.View):
    """Класс финального окна"""

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.manager = None
        self.text_color = arcade.color.CORDOVAN
        self.texts = [
            "Оставшиеся монеты:",
            "Количество оставшихся семян мандрагоры:",
            "Количество оставшихся семян белладонн:",
            "Количество оставшихся семян красных роз:",
            "Количество выращенной мандрагоры:",
            "Количество выращенной балладонны:",
            "Количество выращенной красной розы:",
            "Всего было посажено мандрагор:",
            "Всего было посажено белладонн:",
            "Всего было посажено красной розы:",
            "Количество оставшихся воинов летучих мышей:",
            "Количество оставшихся воинов скелетов:",
            "Количество оставшихся воинов оборотней:",
            "Количество купленных воинов летучих мышей:",
            "Количество купленных воинов скелетов:",
            "Количество купленных воинов оборотней:",
        ]
        self.setup()

    def setup(self):
        self.game_statistic = StatisticData(self.window)  # бд со статистикой игры
        self.time_from_last_frame = 0
        self.frame_number = 0
        self.showed_statistic = False  # Была ли уже показана статистика
        self.rect = arcade.rect.XYWH(
            self.width // 2, self.height // 2, self.width, self.height
        )  # Прямоугольник для дальнейшей отрисовки картинки

        self.all_frames = []
        for i in range(195):
            """Загрузка всех картинок для анимации"""
            frame = arcade.load_texture(f"resources/final/frames/frame_{i}.png")
            self.all_frames.append(frame)
        self.manager = UIManager()

    def on_draw(self):
        """Метод отрисовки картинки"""
        self.clear()
        arcade.draw_texture_rect(self.all_frames[self.frame_number], self.rect)
        if self.manager:
            self.manager.draw()

    def on_update(self, delta_time):
        """Смена кадров с течением времени, если это последний кадр, то пишем статистику"""
        self.time_from_last_frame += delta_time
        if self.time_from_last_frame >= FRAME_DURATION and self.frame_number < 194:
            self.frame_number += 1
            self.time_from_last_frame = 0
        elif self.frame_number == 194 and not self.showed_statistic:
            self.showed_statistic = True
            self.time_from_last_frame = 0
            self.creat_statistic_text()

    def on_key_press(self, symbol, modifiers):
        """Нажатие на любою клавишу - отрисовка последнего текста"""
        if not self.showed_statistic:
            return
        self.box_layout.clear()
        self.anchor_layout.clear()
        self.creat_final_text()

    def creat_statistic_text(self):
        """Метод создания текста статистики"""
        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=20)

        for index, line in enumerate(self.game_statistic.game_information):
            new_line = f"{self.texts[index]} {line}"
            label = UILabel(
                text=new_line,
                font_size=20,
                width=800,
                text_color=self.text_color,
            )
            self.box_layout.add(label)

        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)

    def creat_final_text(self):
        """Метод отрисовки последнего текста"""
        line = self.game_statistic.name
        label = UILabel(
            text=f"{line}, это было непросто, но вы справились!",
            font_size=34,
            width=800,
            align="center",
            text_color=self.text_color,
        )
        self.box_layout.add(label)

        label = UILabel(
            text="Спасибо за игру ;)",
            font_size=34,
            width=800,
            align="center",
            text_color=self.text_color,
        )
        self.box_layout.add(label)

        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)
