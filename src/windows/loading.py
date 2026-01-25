import arcade

DELAY = 0.3  # Задержка для отрисовки фона


class Loading(arcade.View):
    """Класс загрузки"""

    def __init__(self, window, next_view):
        super().__init__()
        self.window = window
        self.next_view = next_view
        self.shown_time = 0
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        arcade.draw_text(
            "Загрузка...", self.width // 2, self.height // 2, arcade.color.WHITE, 24
        )

    def on_update(self, delta_time):
        self.shown_time += delta_time
        if self.shown_time >= DELAY:
            self.window.switch_view(
                self.next_view
            )  # Переключение на следующий вид после отрисовки фона и текста
