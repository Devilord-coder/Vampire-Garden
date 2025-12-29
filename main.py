import arcade
from src.windows.base_window import BaseWindow


def main():
    # Создаем главное окно
    window = BaseWindow()

    # Показываем стартовый экран
    window.switch_view("battle")

    # Запускаем игровой цикл
    arcade.run()


if __name__ == "__main__":
    main()
