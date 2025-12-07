import arcade
import screeninfo
from src.prehistory import Prehistory


# Пример файла, позже будет переключение на другой вид
class MainWindow(arcade.Window):
    def __init__(self):
        monitor = screeninfo.get_monitors()[0]
        width, height = monitor.width, monitor.height
        super().__init__(width, height, "Prehistory View")

    def setup(self):
        view = Prehistory(self)
        self.show_view(view)


def main():
    window = MainWindow()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
