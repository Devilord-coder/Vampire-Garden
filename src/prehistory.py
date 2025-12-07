import arcade
import arcade.gui


class Prehistory(arcade.View):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.sound = arcade.load_sound("resources/sounds/prehistory_sound.mp3")
        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()

    def setup(self):
        # Метод настройки вида (чтение текста предыстрории из файла, загрузка картинок, включение озвучки,
        # создание кнопки для продолжения)
        with open("resources/prehistory.txt", "r") as file:
            self.text = file.readlines()
        self.background = arcade.load_texture("resources/Moon/png/orig.png")
        self.vampire_picture = arcade.load_texture("resources/prehistory_vampire.jpg")
        arcade.play_sound(self.sound, volume=0.5, loop=False)

        button = arcade.gui.UIFlatButton(
            text="Продолжить",
            width=200,
            height=70,
            x=self.width // 2,
            y=self.height // 2 - 20 * self.height // 100,
        )

        button.on_click = self.continue_history
        self.ui_manager.add(button)

    def continue_history(self, event):
        # Метод переключения на следующий вид
        print("OK")
        pass

    def on_show_view(self):
        self.setup()

    def on_draw(self):
        # Метод загрузки текста, картинки и кнопки
        self.clear()
        rect = arcade.rect.XYWH(
            self.width // 2, self.height // 2, self.width, self.height
        )
        arcade.draw_texture_rect(texture=self.background, rect=rect)

        height = self.height // 2 + 50
        for i in range(len(self.text)):
            text = arcade.Text(
                self.text[i],
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
        # Метод отработки изменения окна
        super().on_resize(width, height)
