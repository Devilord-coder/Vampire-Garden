import arcade
from pyglet.graphics import Batch
from src.settings import settings
from src.registry import reg
from arcade import gui


class StartView(arcade.View):
    """Стартовый экран с таймером перехода в главное меню"""

    def __init__(self, window):
        super().__init__()
        self.window = window  # Ссылка на главное окно
        self.login_batch = Batch()
        self.password_batch = Batch()
        self.shape_list = arcade.shape_list.ShapeElementList()
        self.login = None
        self.background = arcade.load_texture('resources/Background/background.jpeg')

    def setup(self):
        """Инициализация представления"""
        
        part_x = self.window.width // 100
        part_y = self.window.height // 100
        center_x = part_x * 50
        center_y = part_y * 50
        
        self.create_text(part_x, part_y, center_x, center_y)
        
        # Создаем объект для ввода логина
        self.login_input = gui.UIInputText(
            x=center_x - part_x * 9, y=center_y + 15 * part_y,
            width=200, height=30,
            text="",  # начальный текст
            font_size=16
        )
        
        # Создаем объект для ввода пароля
        self.password_input = gui.UIInputText(
            x=center_x - part_x * 9, y=center_y - 3 * part_y,
            width=200, height=30,
            text="",  # начальный текст
            font_size=16
        )
        
        # Создаем менеджер GUI
        self.manager = gui.UIManager()
        self.manager.enable()
        
        # Добавляем текстовое поле в менеджер
        self.manager.add(self.password_input)
        self.manager.add(self.login_input)

    def on_show_view(self):
        """Вызывается при показе этого представления"""
        self.setup()

    def on_draw(self):
        """Рисование"""
        self.clear()
        
        arcade.draw_texture_rect(self.background, arcade.rect.XYWH(
            self.width // 2, self.height // 2,
            self.width, self.height
        ))
        
        # Отрисовываем интерфейс
        self.manager.draw()
        self.password_batch.draw()
        self.login_batch.draw()
        self.shape_list.draw()

    def on_update(self, delta_time):
        """Обновление логики"""

        pass

    def on_resize(self, width: float, height: float):
        """Обработка изменения размера окна"""
        super().on_resize(width, height)
        
        part_x = self.window.width // 100
        part_y = self.window.height // 100
        center_x = part_x * 50
        center_y = part_y * 50
        
        self.create_text(part_x, part_y, center_x, center_y)

    def create_text(self, part_x, part_y, center_x, center_y):
        """Создание текста и рамки"""
        # Очищаем предыдущие объекты
        self.login_batch = Batch()
        self.password_batch = Batch()
        if self.shape_list:
            self.shape_list.clear()

        # Расчет размера шрифта
        base_width = settings.width_min
        font_size = int(24 * (self.window.width / base_width))

        # Создаем текст
        self.login = arcade.Text(
            'Login',
            center_x,
            center_y + 26 * part_y,
            arcade.color.ANTIQUE_WHITE,
            font_size,
            bold=True,
            align="center",
            anchor_x="center",
            anchor_y="center",
            batch=self.login_batch
        )
        
        self.password = arcade.Text(
            'Password',
            center_x,
            center_y + 10 * part_y,
            arcade.color.ANTIQUE_WHITE,
            font_size,
            bold=True,
            align="center",
            anchor_x="center",
            anchor_y="center",
            batch=self.password_batch
        )
