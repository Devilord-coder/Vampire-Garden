from src.styles import *
import arcade
import arcade.gui
from src.registry import reg
from arcade.gui import UIManager, UITextureButton, UILabel, UIFlatButton
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout


class StartView(arcade.View):
    """ Стартовый экран для авторизации """

    def __init__(self, window):
        super().__init__()
        self.window = window  # Ссылка на главное окно
        self.background = arcade.load_texture('resources/Background/start_background.jpeg')
        
    def setup(self):
        """Инициализация представления"""
        
        arcade.play_sound(self.window.bg_sound, loop=True, volume=0.75)
        
        self.shape_list = arcade.shape_list.ShapeElementList()
        
        # открываем соединение с БД
        self.window.reg_db.open()
        
        # UIManager — сердце GUI
        self.manager = UIManager()
        self.manager.enable()  # Включить, чтоб виджеты работали
        
        # Layout для организации — как полки в шкафу
        self.anchor_layout = UIAnchorLayout()  # Центрирует виджеты
        self.box_layout = UIBoxLayout(vertical=True, space_between=20)  # Вертикальный стек
        
        # кнопка для регистрации
        reg_btn = UIFlatButton(
            style=button_style,
            text="РЕГИСТРАЦИЯ",
            width=200
        )
        
        # Это пока тестовый вариант кнопки (потом я её уменьшу)
        texture_normal = arcade.load_texture("resources/buttons/OK/OK_Default.png")
        texture_hovered = arcade.load_texture("resources/buttons/OK/OK_Hovered.png")
        texture_pressed = arcade.load_texture("resources/buttons/OK/OK_Hovered.png")
        self.log_in_btn = UITextureButton(texture=texture_normal, 
                                        texture_hovered=texture_hovered,
                                        texture_pressed=texture_pressed,
                                        scale=1.0)
        
        # при нажатии кнопки окно меняется на регистрацию
        @reg_btn.event("on_click")
        def on_click_settings(event):
            self.error_text.text = ""
            self.window.switch_view("registration")
            arcade.play_sound(reg.button_click_sound)
        
        # при нажатии войти
        @self.log_in_btn.event("on_click")
        def on_click_settings(event):
            result, error = self.check_user()
            if result:
                self.error_text.text = ""
                self.error_shadow.text = ""
                self.window.reg_db.close()
                self.window.switch_view("main_menu")
                self.login = self.login_input.text
                arcade.play_sound(reg.button_click_sound)
            else:
                self.error_text.text = error.upper()
                self.error_shadow.text = error.upper()
                ... # звук ошибки
        
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
        
        # надпись логин
        login_text = UILabel(
            text='ЛОГИН',
            text_color=TEXT_COLOR,
            font_size=18,
            multiline=True
        )
        
        # надпись пароль
        password_text = UILabel(
            text='ПАРОЛЬ',
            text_color=TEXT_COLOR,
            font_size=18,
            multiline=True
        )
        
        # объект для ввода логина
        self.login_input = arcade.gui.UIInputText(
            width=300, height=30,
            text="",
            font_size=FONT_SIZE,
            style=input_text_style,
            text_color=TEXT_COLOR,
            border_color=TEXT_COLOR
        )
        
        # объект для ввода пароля
        self.password_input = arcade.gui.UIInputText(
            width=300, height=30,
            text="",
            font_size=FONT_SIZE,
            style=input_text_style,
            text_color=TEXT_COLOR,
            border_color=TEXT_COLOR
        )
        
        # ==== ДОБАВЛЯЕМ ВИДЖЕТЫ ПО ПОРЯДКУ ====
        self.box_layout.add(login_text)
        self.box_layout.add(self.login_input)
        self.box_layout.add(password_text)
        self.box_layout.add(self.password_input)
        self.box_layout.add(self.log_in_btn)
        self.box_layout.add(reg_btn)
        
        self.anchor_layout.add(self.box_layout)  # Box в anchor
        self.manager.add(self.anchor_layout)  # Всё в manager
    
    def check_user(self) -> tuple[bool, None | str]:
        """ Функция для проверки введенного пароля и логина

        Returns:
            tuple[bool, None | str]: результат и ошибка (если есть)
        """

        login = self.login_input.text
        password = self.password_input.text
        if not login or not password:
            return False, "Все поля должны быть заполнены"
        result = self.window.reg_db.check_user(login, password)
        if result == "OK":
            return True, None
        else:
            return False, result

    def on_show_view(self):
        """Вызывается при показе этого представления"""

        self.setup()

    def on_draw(self):
        """Рисование"""
        self.clear()
        
        # ------------- ЗАДНИЙ ФОН -------------
        arcade.draw_texture_rect(self.background, arcade.rect.XYWH(
            self.width // 2, self.height // 2,
            self.width, self.height
        ))
        
        # --- ПОСЛЕ ЗАДНЕГО ФОНА ВСЕ ОСТАЛЬНОЕ ---
        self.manager.draw()
        self.shape_list.draw()
        self.error_shadow.draw()
        self.error_text.draw()

    def on_update(self, delta_time):
        """Обновление логики"""

        ...
    
    def on_resize(self, width, height):
        """ Изменение размера окна """
        
        super().on_resize(width, height)
        self.setup()