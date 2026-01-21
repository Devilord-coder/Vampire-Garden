import arcade
from src.registry import reg
from datetime import datetime

DELAY_TIME = 1


class TutorialView(arcade.View):
    """Класс туториала"""

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.setup()

    def setup(self):
        """Загрузка ресурсов"""
        self.time_from_last_slide = 0
        self.slide_number = 0
        self.rect = arcade.rect.XYWH(
            self.width // 2, self.height // 2, self.width, self.height
        )  # Объект прямоугольника для дальнейшей отрисовки

        self.all_photos = []
        self.all_audios = reg.tutorial_sounds
        for i in range(8):
            photo = arcade.load_texture(f"resources/tutorial/photos/photo{i}.jpg")
            self.all_photos.append(photo)

        self.current_sound = None
        self.slide_duration = None

    def on_draw(self):
        """Метод отрисовки картинки"""
        self.clear()
        arcade.draw_texture_rect(self.all_photos[self.slide_number], self.rect)

    def next_slide(self):
        """Метод смены слайдов"""
        self.slide_number += 1
        self.time_from_last_slide = 0
        arcade.stop_sound(self.current_sound)  # Отключение предыдущего звука
        arcade.play_sound(
            reg.book_sound, 0.4, loop=False
        )  # Звук перехода на другую страницу
        if self.slide_number == len(self.all_photos):
            # Переключение на главную карту, если туториал закончился
            self.window.switch_view("main_map")
            return
        self.current_sound = arcade.play_sound(
            self.all_audios[self.slide_number], 1, loop=False
        )  # Проигрыш нового звука
        self.slide_duration = (
            self.current_sound.source.duration + DELAY_TIME
        )  # Определение времени показа слайда по длине звука

    def on_update(self, delta_time):
        """Обновление времени с предыдущего слайда, смена слайда по истечении времени"""
        if not self.slide_duration:  # Если звука не было, включаем
            self.current_sound = arcade.play_sound(
                self.all_audios[self.slide_number], 1, loop=False
            )
            self.slide_duration = (
                self.current_sound.source.duration + DELAY_TIME
            )  # Время показа слайда по длине звука
            self.time_from_last_slide = 0

        self.time_from_last_slide += delta_time

        if self.time_from_last_slide > self.slide_duration:  # По истечении времени
            self.next_slide()

    def on_key_press(self, symbol, modifiers):
        """При нажатии на пробел, переключаем слайд"""
        if symbol == arcade.key.SPACE:
            self.next_slide()
