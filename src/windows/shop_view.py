import arcade
from pyglet.graphics import Batch
import arcade.gui
from data import ShopData
from src.auxiliary_classes.scale import scale
from src.settings import settings
from src.registry import reg

MANDRAGORA_PRICE = 20
BELLADONNA_PRICE = 50
ROSE_PRICE = 100
ERROR_TIME_VISIBLE = 1

PLATS_SCALE = scale(540, settings.height)
PRICELIST_SCALE = scale(300, settings.height)
EXIT_SCALE = scale(120, settings.height)


class ShopView(arcade.View):
    """Представление магазина для покупки семян"""

    def __init__(self, window):
        """Инициализация представления, переменные из прошлых окон, загрузка текстур, координаты кнопок"""

        self.window = window
        self.batch = Batch()
        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()
        self.error = False

        self.backgound_texture = arcade.load_texture(
            "resources/Background/shop_background.png"
        )
        self.madragora_texture = arcade.load_texture(
            "resources/shop_pictures/mandragora.png"
        )
        self.belladonna_texture = arcade.load_texture(
            "resources/shop_pictures/belladonna.png"
        )
        self.rose_texture = arcade.load_texture("resources/shop_pictures/rose.png")
        self.pricelist_texture = arcade.load_texture(
            "resources/shop_pictures/pricelist.png"
        )
        self.money_texture = arcade.load_texture("resources/money.png")
        self.cart_texture = arcade.load_texture("resources/shop_pictures/cart.png")
        self.exit_texture = arcade.load_texture("resources/buttons/exit/shop_exit.png")

        self.door_sound = reg.door_sound
        self.buy_sound = reg.buy_sound
        self.sad_sound = reg.sad_sound  # Звук при недостатке средств во время покупки

        width = self.width // 2 - 200
        height = self.height // 2 - 150
        delta_width = width // 2 - 70
        delta_height = height // 2 - 10
        self.plants = {
            "mandragora": (
                self.width // 4 + delta_width,
                self.height // 4 - delta_height,
            ),
            "belladonna": (
                self.width // 4 + delta_width,
                self.height - self.height // 4 - delta_height,
            ),
            "rose": (
                self.width - self.width // 4 + delta_width,
                self.height // 4 - delta_height,
            ),
        }

        self.setup()

    def setup(self):
        """Загрузка представления, подготовка всех текстов"""
        
        self.information = ShopData(self.window)
        self.left_money = self.information.quantity_money
        self.quantity_mandragora = self.information.quantity_mandragora_seeds
        self.quantity_belladonna = self.information.quantity_belladonna_seeds
        self.quantity_rose = self.information.quantity_rose_seeds

        x = 80
        y = self.height - 60
        self.left_money_text = arcade.Text(
            str(self.left_money), x, y, arcade.color.WHITE, 50, batch=self.batch
        )
        self.error_text = arcade.Text(
            "Недостаточно средств!",
            self.width // 4,
            self.height // 2,
            arcade.color.RED,
            50,
            batch=None,
        )
        self.error = True
        self.error_time = 0
        for plant in self.plants.keys():
            x, y = self.plants[plant]
            self.buttons_init(plant, x, y)
        self.exit_button_init()

    def exit_button_init(self):
        """Инициализация кнопки для перехода на представление главной карты"""
        x = self.width // 2 - self.exit_texture.width // 2
        y = self.height // 2 - self.exit_texture.height // 2
        button = arcade.gui.UITextureButton(
            x=x,
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

        self.ui_manager.add(button)

    def buttons_init(self, plant, x, y):
        """Инициализация кнопок для покупки семян"""
        button = arcade.gui.UITextureButton(
            x=x,
            y=y,
            texture=self.cart_texture,
            texture_hovered=self.cart_texture,
            texture_pressed=self.cart_texture,
            scale=PLATS_SCALE,
        )
        button.name = plant

        @button.event("on_click")
        def on_click(event):
            have_bought = False
            plant = event.source.name
            if plant == "mandragora":
                self.left_money -= MANDRAGORA_PRICE
                if self.left_money < 0:
                    self.left_money += MANDRAGORA_PRICE
                    self.error_text.batch = self.batch
                else:
                    self.quantity_mandragora += 1
                    self.information.quantity_mandragora_seeds = (
                        self.quantity_mandragora
                    )
                    have_bought = True
            elif plant == "belladonna":
                self.left_money -= BELLADONNA_PRICE
                if self.left_money < 0:
                    self.left_money += BELLADONNA_PRICE
                    self.error_text.batch = self.batch
                else:
                    self.quantity_belladonna += 1
                    self.information.quantity_belladonna_seeds = (
                        self.quantity_belladonna
                    )
                    have_bought = True
            elif plant == "rose":
                self.left_money -= ROSE_PRICE
                if self.left_money < 0:
                    self.left_money += ROSE_PRICE
                    self.error_text.batch = self.batch
                else:
                    self.quantity_rose += 1
                    self.information.quantity_rose_seeds = self.quantity_rose
                    have_bought = True

            if have_bought:
                # Если покупка удалась -> звук покупки
                arcade.play_sound(self.buy_sound, 1, loop=False)
            else:
                # Инче -> звук грусти
                arcade.play_sound(self.sad_sound, 1, loop=False)
            self.left_money_text.text = str(self.left_money)
            self.information.quantity_money = self.left_money
            self.information.save()

        self.ui_manager.add(button)

    def on_draw(self):
        """Отрисовка всех картинок, текстов, кнопок"""

        rect = arcade.rect.XYWH(
            self.width // 2, self.height // 2, self.width, self.height
        )
        arcade.draw_texture_rect(self.backgound_texture, rect)

        width = self.width // 2 - 200
        height = self.height // 2 - 150

        rect = arcade.rect.XYWH(self.width // 4, self.height // 4, width, height)
        arcade.draw_texture_rect(self.madragora_texture, rect)

        rect = arcade.rect.XYWH(
            self.width // 4, self.height - self.height // 4, width, height
        )
        arcade.draw_texture_rect(self.belladonna_texture, rect)

        rect = arcade.rect.XYWH(
            self.width - self.width // 4, self.height // 4, width, height
        )
        arcade.draw_texture_rect(self.rose_texture, rect)

        width -= 200
        height = self.height - self.height // 2
        rect = arcade.rect.XYWH(
            self.width - self.width // 4,
            self.height - self.height // 4 - 50,
            width,
            height,
        )
        arcade.draw_texture_rect(self.pricelist_texture, rect)

        rect = arcade.rect.XYWH(40, self.height - 40, 60, 60)
        arcade.draw_texture_rect(self.money_texture, rect)

        self.ui_manager.draw()
        self.batch.draw()

    def on_update(self, delta_time):
        """Обновление логики"""

        if self.error:
            self.error_time += delta_time
        if self.error_time >= ERROR_TIME_VISIBLE:
            self.error_text.batch = None
            self.error_time = 0

    def on_show_view(self):
        """Активация ui менеджера"""
        if self.ui_manager:
            self.ui_manager.enable()

    def on_hide_view(self):
        """Выключение ui менеджера"""
        if self.ui_manager:
            self.ui_manager.disable()
