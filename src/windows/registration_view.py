from src.styles import *
import arcade
import arcade.gui
from arcade.gui import UIManager, UITextureButton, UILabel, UIFlatButton
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout


class RegistrationView(arcade.View):
    """ Экран для регистрации """

    def __init__(self, window):
        super().__init__()
        self.window = window  # Ссылка на главное окно
        self.background = arcade.load_texture('resources/Background/start_background.jpeg')

    def setup(self):
        """Инициализация представления"""
        
        # UIManager — сердце GUI
        self.manager = UIManager()
        self.manager.enable()  # Включить, чтоб виджеты работали
        
        # Layout для организации — как полки в шкафу
        self.anchor_layout = UIAnchorLayout()  # Центрирует виджеты
        self.box_layout = UIBoxLayout(vertical=True, space_between=20)  # Вертикальный стек
        
        reg_btn = UIFlatButton(
            style=button_style,
            text="ЗАРЕГИСТРИРОВАТЬСЯ",
            width=200
        )
        
        # при нажатии кнопки окно меняется на регистрацию
        @reg_btn.event("on_click")
        def on_click_settings(event):
            result, error = self.add_user()
            if result:
                self.error_text.text = ""
                self.error_shadow.text = ""
                self.window.switch_view("start")
            else:
                self.error_text.text = error.upper()
                self.error_shadow.text = error.upper()
            
        name_text = UILabel(
            text='Имя',
            text_color=arcade.color.AMARANTH_PURPLE,
            font_size=30,
            multiline=True
        )
        
        # объект для ввода имени
        self.name_input = arcade.gui.UIInputText(
            width=300, height=30,
            text="",
            font_size=FONT_SIZE,
            style=input_text_style,
            text_color=arcade.color.AMARANTH_PURPLE,
            border_color=arcade.color.AMARANTH_PURPLE
        )
        
        email_text = UILabel(
            text='Почта',
            text_color=arcade.color.AMARANTH_PURPLE,
            font_size=30,
            multiline=True
        )
        
        # объект для ввода имени
        self.email_input = arcade.gui.UIInputText(
            width=300, height=30,
            text="",
            font_size=FONT_SIZE,
            style=input_text_style,
            text_color=arcade.color.AMARANTH_PURPLE,
            border_color=arcade.color.AMARANTH_PURPLE
        )
        
        # надпись логин
        login_text = UILabel(
            text='Логин',
            text_color=arcade.color.AMARANTH_PURPLE,
            font_size=30,
            multiline=True
        )
        
        # надпись пароль
        password_text = UILabel(
            text='Пароль',
            text_color=arcade.color.AMARANTH_PURPLE,
            font_size=30,
            multiline=True
        )
        
        # объект для ввода логина
        self.login_input = arcade.gui.UIInputText(
            width=300, height=30,
            text="",
            font_size=FONT_SIZE,
            style=input_text_style,
            text_color=arcade.color.AMARANTH_PURPLE,
            border_color=arcade.color.AMARANTH_PURPLE
        )
        
        # объект для ввода пароля
        self.password_input = arcade.gui.UIInputText(
            width=300, height=30,
            text="",
            font_size=FONT_SIZE,
            style=input_text_style,
            text_color=arcade.color.AMARANTH_PURPLE,
            border_color=arcade.color.AMARANTH_PURPLE
        )
        
        part_x, part_y, c_x, c_y = self.window.get_parts()
        self.error_text = arcade.Text(
            text="",
            font_size=18,
            multiline=True,
            width=500,
            x=c_x - 15 * part_x,
            y=90 * part_y,
            color=TEXT_COLOR
        )
        self.error_shadow = arcade.Text(
            text="",
            font_size=18,
            multiline=True,
            width=500,
            x=c_x - 15 * part_x + 3,
            y=90 * part_y,
            color=arcade.color.BLACK
        )
        
        # ==== ДОБАВЛЯЕМ ВИДЖЕТЫ ПО ПОРЯДКУ ====
        self.box_layout.add(name_text)
        self.box_layout.add(self.name_input)
        self.box_layout.add(email_text)
        self.box_layout.add(self.email_input)
        self.box_layout.add(login_text)
        self.box_layout.add(self.login_input)
        self.box_layout.add(password_text)
        self.box_layout.add(self.password_input)
        self.box_layout.add(reg_btn)
        
        self.anchor_layout.add(self.box_layout)  # Box в anchor
        self.manager.add(self.anchor_layout)  # Всё в manager
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.switch_view("start")

    def add_user(self) -> tuple[bool, None | str]:
        """ Добавление пользователя в БД

        Returns:
            tuple[bool, None | str]: результат и ошибка (если есть)
        """

        name = self.name_input.text
        email = self.email_input.text
        login = self.login_input.text
        password = self.password_input.text
        
        result =  self.window.reg_db.add_user(name, email, login, password)
        if result == "OK":
            return True, None
        else:
            return False, result

    def on_show_view(self):
        """Вызывается при показе этого представления"""

        self.setup()

    def on_draw(self):
        """Рисование"""
        
        # Очищаем
        self.clear()
        
        # ------------- ЗАДНИЙ ФОН -------------
        arcade.draw_texture_rect(self.background, arcade.rect.XYWH(
            self.width // 2, self.height // 2,
            self.width, self.height
        ))
        
        # только после этого все остальное
        self.manager.draw()
        self.error_shadow.draw()
        self.error_text.draw()

    def on_update(self, delta_time):
        """Обновление логики"""

        ...
    
    def on_resize(self, width, height):
        """ Изменение размера окна """
        
        super().on_resize(width, height)
        self.setup()
