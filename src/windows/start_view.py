from src.settings import settings
from src.registry import reg
import src.styles as styles
import arcade
import arcade.gui
import arcade.gui.widgets.buttons
from arcade.gui import UIManager, UIFlatButton, UITextureButton, UILabel, UIInputText, UITextArea, UISlider, UIDropdown, \
    UIMessageBox  # Это разные виджеты
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout  # А это менеджеры компоновки, как в pyQT


class StartView(arcade.View):
    """ Стартовый экран для авторизации """

    def __init__(self, window):
        super().__init__()
        self.window = window  # Ссылка на главное окно
        self.background = arcade.load_texture('resources/Background/background.jpeg')
        
    def setup(self):
        """Инициализация представления"""
        
        # UIManager — сердце GUI
        self.manager = UIManager()
        self.manager.enable()  # Включить, чтоб виджеты работали
        
        # Layout для организации — как полки в шкафу
        self.anchor_layout = UIAnchorLayout()  # Центрирует виджеты
        self.box_layout = UIBoxLayout(vertical=True, space_between=20)  # Вертикальный стек

        part_x, part_y, center_x, center_y = self.get_parts()

        # кнопка для входа
        log_in_btn = arcade.gui.widgets.buttons.UIFlatButton(
            x=center_x - 11 * part_x,
            y=center_y - 12 * part_y,
            style=styles.button_style,
            text="Войти", width=200
        )
        
        # кнопка для регистрации
        reg_btn = arcade.gui.widgets.buttons.UIFlatButton(
            x=center_x + 5 * part_x,
            y=center_y - 12 * part_y,
            style=styles.button_style,
            text="Регистрация", width=200
        )
        
        texture_normal = arcade.load_texture("resources/buttons/OK/OK_Default.png")
        texture_hovered = arcade.load_texture("resources/buttons/OK/OK_Hovered.png")
        texture_pressed = arcade.load_texture("resources/buttons/OK/OK_Hovered.png")
        log_in_btn = UITextureButton(texture=texture_normal, 
                                        texture_hovered=texture_hovered,
                                        texture_pressed=texture_pressed,
                                        scale=1.0)
        
        # при нажатии кнопки окно меняется на регистрацию
        @reg_btn.event("on_click")
        def on_click_settings(event):
            self.window.switch_view("registration")
        
        # при нажатии войти
        @log_in_btn.event("on_click")
        def on_click_settings(event):
            ... # проверка есть ли такой пользователь
            self.window.switch_view("main_menu")
        
        # надпись логин
        login_text = UILabel(
            text='Логин',
            x=center_x - part_x * 10,
            y=center_y + 23 * part_y,
            text_color=arcade.color.AMARANTH_PURPLE,
            font_size=30
        )
        
        # надпись пароль
        password_text = UILabel(
            text='Пароль',
            x=center_x - 10 * part_x,
            y=center_y + 5 * part_y,
            text_color=arcade.color.AMARANTH_PURPLE,
            font_size=30
        )
        
        # объект для ввода логина
        login_input = arcade.gui.UIInputText(
            x=center_x - part_x * 9, y=center_y + 15 * part_y,
            width=300, height=30,
            text="",
            font_size=16,
            style=styles.input_text_style,
            text_color=arcade.color.AMARANTH_PURPLE,
            border_color=arcade.color.AMARANTH_PURPLE
        )
        
        # объект для ввода пароля
        password_input = arcade.gui.UIInputText(
            x=center_x - part_x * 9, y=center_y - 3 * part_y,
            width=300, height=30,
            text="",
            font_size=16,
            style=styles.input_text_style,
            text_color=arcade.color.AMARANTH_PURPLE,
            border_color=arcade.color.AMARANTH_PURPLE
        )
        
        self.box_layout.add(login_text)
        self.box_layout.add(login_input)
        self.box_layout.add(password_text)
        self.box_layout.add(password_input)
        self.box_layout.add(reg_btn)
        self.box_layout.add(log_in_btn)
        
        self.anchor_layout.add(self.box_layout)  # Box в anchor
        self.manager.add(self.anchor_layout)  # Всё в manager
    
    def get_parts(self) -> tuple[int, int, int, int]:
        """ Функция для разделения экрана на равные части

        Returns:
            tuple[int, int, int, int]: одна сотая часть экрана по х и у,
        а также центры окна по х и у
        """

        # part_x и part_y - одна сотая часть экрана по х и у,
        # так будет легче ставить кнопки на разных размерах экрана
        part_x = self.window.width // 100
        part_y = self.window.height // 100
        center_x = part_x * 50
        center_y = part_y * 50
        
        return (part_x, part_y, center_x, center_y)

    def on_show_view(self):
        """Вызывается при показе этого представления"""

        self.setup()

    def on_draw(self):
        """Рисование"""
        self.clear()
        
        # рисуем задний фон
        arcade.draw_texture_rect(self.background, arcade.rect.XYWH(
            self.width // 2, self.height // 2,
            self.width, self.height
        ))
        
        # только после этого все остальное
        self.manager.draw()

    def on_update(self, delta_time):
        """Обновление логики"""

        ...
    
    def on_resize(self, width, height):
        """ Изменение размера окна """
        
        super().on_resize(width, height)
        self.setup()
