import arcade
from arcade.gui import UIManager, UITextureButton, UILabel
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout
from pyglet.graphics import Batch

from data.statistic_data import StatisticData
from src.auxiliary_classes.scale import scale
from src.settings import settings
from src.registry import reg

TEXTURE_TIME = 0.1  # Таймер смены текстур
ERROR_TIME_VISIBLE = 1  # Время отображения текста ошибки
EXIT_SCALE = scale(120, settings.height)
BUY_SCALE = 1


class Building(arcade.View):
    def __init__(self):
        super().__init__()
        self.level = 0
        self.req_list = [[] for _ in range(6)]
        self.minion_name = None
        self.textures = None
        self.prices = {"bat": 20, "sceleton": 60, "werewolf": 120}
        self.current_texture = 0
        self.time = 0
        self.error = False
        self.error_text = None
        self.error_time = 0

        self.background_texture = arcade.load_texture(
            "resources/Background/minions_shops.jpeg"
        )
        self.exit_texture = arcade.load_texture("resources/buttons/exit/shop_exit.png")
        self.buy_texture = arcade.load_texture("resources/buttons/buy.png")
        self.paper_texture = arcade.load_texture("resources/Background/paper.png")
        
        self.door_sound = reg.door_sound
        self.buy_sound = reg.buy_sound

        self.texts = [
            "Добро пожаловать!",
            "Ваши накопления составляют:",
            "Стоимость воина:",
        ]
        self.text_color = arcade.color.CORDOVAN
        self.setup()

    def setup(self):
        """Подготовка вида к дальнейшей работе"""
        self.manager = UIManager()
        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=20)
        self.batch = Batch()

        self.game_statistic = StatisticData(self.window)
        self.exit_button_init()

        self.error_text = arcade.Text(
            "Недостаточно средств!",
            self.width // 4,
            self.height // 2,
            arcade.color.RED,
            50,
            batch=None,
        )

        if not self.minion_name:
            return
        self.error = True
        self.error_time = 0
        self.create_text()

    def create_text(self):
        """Заполнение виджетов текстами и данными из бд"""
        self.quantity_money = self.game_statistic.get_quntity_money()
        information = [None, self.quantity_money, self.prices[self.minion_name]]
        for index, info in enumerate(information):
            if not info:
                text = self.texts[index]
            else:
                text = f"{self.texts[index]} {info}"
            label = UILabel(
                text=text,
                font_size=26,
                width=800,
                text_color=self.text_color,
            )
            self.box_layout.add(label)

        self.buy_button_init()
        self.anchor_layout.add(self.box_layout, anchor_x="right")
        self.manager.add(self.anchor_layout)

    def buy_button_init(self):
        """Кнопка для покупки бойца"""
        button = UITextureButton(
            texture=self.buy_texture,
            texture_hovered=self.buy_texture,
            texture_pressed=self.buy_texture,
            scale=BUY_SCALE,
        )

        @button.event("on_click")
        def on_click(event):
            arcade.play_sound(self.buy_sound, 1, loop=False)
            if (
                self.quantity_money - self.prices[self.minion_name]
            ) < 0:  # Отрисовка текста ошибке при недостатке средств
                self.error = True
                self.error_text.batch = self.batch
                return
            self.quantity_money -= self.prices[self.minion_name]
            self.game_statistic.update_minions_information(
                self.minion_name, self.quantity_money
            )
            self.box_layout.clear()
            self.anchor_layout.clear()
            self.game_statistic.update()
            self.create_text()

        self.box_layout.add(button)

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

    def building_init(self, minion_name, textures):
        """Первоначальные данные для различия зданий"""
        self.minion_name = minion_name
        self.textures = textures
        self.texture = self.textures[self.current_texture]

    def on_update(self, delta_time):
        self.time += delta_time
        if self.time >= TEXTURE_TIME:  # Смена текстур
            self.current_texture = (self.current_texture + 1) % len(self.textures)
            self.texture = self.textures[self.current_texture]
            self.time = 0

        # Проверка для скрытия текста ошибки
        if self.error:
            self.error_time += delta_time
        if self.error_time >= ERROR_TIME_VISIBLE:
            self.error = False
            self.error_text.batch = None
            self.error_time = 0

    def on_draw(self):
        """Отрисовка фона, бойца, текста, кнопок"""
        self.clear()
        rect = arcade.rect.XYWH(
            self.width // 2, self.height // 2, self.width, self.height
        )
        arcade.draw_texture_rect(self.background_texture, rect)

        rect = arcade.rect.XYWH(self.width // 3, self.height // 2, 1000, 800)
        arcade.draw_texture_rect(self.texture, rect)

        width = 700
        height = 400
        x = self.width - width // 2 + 50
        y = self.height // 2
        rect = arcade.rect.XYWH(x, y, width, height)
        arcade.draw_texture_rect(self.paper_texture, rect)

        self.manager.draw()
        self.batch.draw()

    def on_show_view(self):
        """Активация ui менеджера"""
        if self.manager:
            self.manager.enable()
            self.box_layout.clear()
            self.anchor_layout.clear()
            self.game_statistic.update()
            self.create_text()

    def on_hide_view(self):
        """Выключение ui менеджера"""
        if self.manager:
            self.manager.disable()
