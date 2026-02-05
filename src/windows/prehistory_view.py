import arcade
import arcade.gui
import src.styles as styles
from src.registry import reg


class PrehistoryView(arcade.View):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.sound = reg.prehistory_voice
        self.book_sound = reg.book_sound
        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()
        self.setup()

    def setup(self):
        """Метод настройки вида (чтение текста предыстрории из файла, загрузка картинок, включение озвучки,
        создание кнопки для продолжения)"""

        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()

        # настройка текста сообщения
        self.text = """Всё началось с того, что мой любимый питомец заболел.
Тогда я прочитал в книге, что ему может помочь только одно зелье,
но у меня не было ингредиентов, и я не знал, где их найти. Я решил сам их вырастить...""".split('\n')
        self.background = arcade.load_texture("resources/Moon/orig.png")
        self.vampire_picture = arcade.load_texture("resources/prehistory_vampire.jpg")
        self.voice_playback = arcade.play_sound(self.sound, volume=0.9, loop=False)

        part_x, part_y, center_x, center_y = self.window.get_parts()

        # кнопка продолжить
        button = arcade.gui.UIFlatButton(
            text="Продолжить",
            width=20 * part_x,
            height=7 * part_y,
            x=center_x - 10 * part_x,
            y=center_y - 15 * part_y,
            style=styles.button_style,
        )

        button.on_click = self.continue_history
        self.ui_manager.add(button)

    def continue_history(self, event):
        """Метод переключения на следующий вид"""

        arcade.play_sound(self.book_sound, 1, loop=False)
        #  при нажатии прекратить голос и переключиться на карту
        arcade.stop_sound(self.voice_playback)
        self.ui_manager.disable()
        self.window.switch_view("tutorial")  # переключение на туториал

    def on_show_view(self):
        self.setup()

    def on_draw(self):
        """Метод загрузки текста, картинки и кнопки"""
        self.clear()
        rect = arcade.rect.XYWH(
            self.width // 2, self.height // 2, self.width, self.height
        )
        arcade.draw_texture_rect(texture=self.background, rect=rect)

        height = self.height // 2 + 50
        for i in range(len(self.text)):
            text = arcade.Text(
                self.text[i] + '\n',
                self.width // 2 - 10 * self.width // 100,
                height,
                font_size=20,
                color=arcade.color.WHITE,
                anchor_x="center",
                anchor_y="center",
                font_name="Calibri",
                italic=True,
            )
            text.draw()
            height -= 50

        rect = arcade.rect.XYWH(
            self.width // 2 + 40 * self.width // 100, self.height // 2, 280, 500
        )
        arcade.draw_texture_rect(texture=self.vampire_picture, rect=rect)

        self.ui_manager.draw()

    def on_resize(self, width: float, height: float):
        """Метод отработки изменения окна"""
        super().on_resize(width, height)

    def on_show_view(self):
        """Активация ui менеджера"""
        if self.ui_manager:
            self.ui_manager.enable()

    def on_hide_view(self):
        """Выключение ui менеджера"""
        if self.ui_manager:
            self.ui_manager.disable()
