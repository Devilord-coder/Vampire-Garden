import arcade
from src.windows.base_window import BaseWindow


if __name__ == "__main__":
    # Создаем главное окно
    window = BaseWindow()

    # Показываем стартовый экран
    window.switch_view("start")

    # Запускаем игровой цикл
    arcade.run()
