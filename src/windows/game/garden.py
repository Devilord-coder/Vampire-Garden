import arcade
import random
from arcade.gui import UITextArea, UIManager, UITextureButton

from src.auxiliary_classes.scale import scale
from data.garden_data import GardenData
from src.settings import settings
from src.windows.game.sprites.rabbit import Rabbit

FIELD_SCALE = scale(300, settings.height)
SEED_SCALE = scale(200, settings.height)
EXIT_SCALE = scale(200, settings.height)


class GardenView(arcade.View):
    """Класс огорода"""

    def __init__(self, window):
        self.window = window
        self.background_color = arcade.color.BLACK
        self.manager = None
        self.garden_information = None

        self.background_texture = arcade.load_texture(
            "resources/Background/garden.jpeg"
        )
        self.empty_field_texture = arcade.load_texture(
            "resources/garden/fields/empty.jpg"
        )
        self.sprouts_field_texture = arcade.load_texture(
            "resources/garden/fields/sprouts.jpg"
        )
        self.mandragora_field_texture = arcade.load_texture(
            "resources/garden/fields/mandragora.jpg"
        )
        self.belladonna_field_texture = arcade.load_texture(
            "resources/garden/fields/belladonna.jpg"
        )
        self.rose_field_texture = arcade.load_texture(
            "resources/garden/fields/rose.jpg"
        )

        self.mandragora_seeds_texture = arcade.load_texture(
            "resources/garden/seeds/mandragora.png"
        )
        self.belladonna_seeds_texture = arcade.load_texture(
            "resources/garden/seeds/belladonna.png"
        )
        self.rose_seeds_texture = arcade.load_texture("resources/garden/seeds/rose.png")
        self.shovel_texture = arcade.load_texture("resources/garden/seeds/shovel.png")

        self.exit_texture = arcade.load_texture(
            "resources/buttons/exit/garden_back.png"
        )

        self.seeds_textures = [
            self.shovel_texture,
            self.mandragora_seeds_texture,
            self.belladonna_seeds_texture,
            self.rose_seeds_texture,
        ]
        self.current_seed_texture = 0
        self.timers = {
            "Мандрагора": 20,
            "Белладонна": 40,
            "Красная роза": 60,
        }  # Таймеры, которые показывают через сколько растение вырастет после посадки
        self.plants_timers = {}  # Таймеры для роста растений

        self.time_from_last_rabbit = 0
        self.next_rabbit = random.randint(180, 200)
        self.setup()

    def setup(self):
        """Инициализация, создание визуального представления огорода, ссылаясь на бд"""
        self.manager = UIManager()
        self.manager.enable()
        self.exit()

        self.fields_list = arcade.SpriteList()
        self.seed_list = arcade.SpriteList()
        self.rabbits_list = arcade.SpriteList()
        self.garden_information = GardenData(self.window)
        self.database_setting()

        # Создание каждой грядки
        field_number = 0
        y = self.height - 0.1 * self.height - self.empty_field_texture.height // 2
        for _ in range(2):
            x = self.width * 0.05 + self.empty_field_texture.width // 2
            for _ in range(3):
                field = arcade.Sprite(self.empty_field_texture, FIELD_SCALE, x, y)
                field.number = field_number  # Номер грядки
                field.busy = False  # Есть ли кролик на грядке
                field.time_with_rabbit = 0  # Время, которое кролик был на грядке
                field.quantity_bites = self.garden_information.fields[field_number][
                    "quantity_bites"
                ]  # Количество укусов
                field.rabbit = None  # Кролик на грядке
                self.choose_texture(field, field_number)
                self.fields_list.append(field)
                x += self.empty_field_texture.width + 0.05 * self.width
                field_number += 1
            y = 0.1 * self.height + self.empty_field_texture.height // 2

        x = self.width * 0.16 + self.empty_field_texture.width * 3
        y = self.height - 0.1 * self.height - self.empty_field_texture.height // 2
        self.quantity_text = UITextArea(
            text=f"Мандрагора - {self.quantity_mandragora}\n"
            f"Белладонна - {self.quantity_belladonna}\n"
            "Красная роза - {self.quantity_rose}",
            x=x + 20,
            y=y,
            font_size=20,
            text_color=arcade.color.LIGHT_BLUE,
            height=100,
        )
        self.manager.add(self.quantity_text)

        # Спрайт для посадки семян и их сбора
        self.seed = arcade.Sprite(
            self.seeds_textures[self.current_seed_texture],
            SEED_SCALE,
            self.width - (self.width - x) // 2,
            self.height // 2,
        )
        self.seed_list.append(self.seed)

        for _ in range(4):
            self.create_rabbit()

    def on_draw(self):
        self.clear()
        rect = arcade.rect.XYWH(
            self.width // 2, self.height // 2, self.width, self.height
        )
        arcade.draw_texture_rect(self.background_texture, rect)

        self.fields_list.draw()
        self.seed_list.draw()
        self.manager.draw()
        self.rabbits_list.draw()

    def on_update(self, delta_time):
        """Обновление кроликов, проверка пересечения кролика с грядкой, поедание урожая"""
        self.time_from_last_rabbit += delta_time
        for rabbit in self.rabbits_list:
            # Обновление состояния каждого кролика
            rabbit.update(delta_time)

        if self.time_from_last_rabbit >= self.next_rabbit:
            # Создание кроликов через определённый промежуток времени
            quantity_rabbits = random.randint(1, 3)
            for _ in range(quantity_rabbits):
                self.create_rabbit()
            self.time_from_last_rabbit = 0
            self.next_rabbit = random.randint(180, 200)

        for rabbit in self.rabbits_list:
            # Проверяем пересечение кролика с грядкой
            if rabbit.state == "run" or rabbit.state == "idle":
                continue
            fields = arcade.check_for_collision_with_list(rabbit, self.fields_list)
            for field in fields:
                # Проверка возможности занять эту грядку, если да, обновляем атрибуты
                if (
                    not field.busy
                    and self.garden_information.fields[field.number]["state"] != 0
                ):
                    field.rabbit = rabbit
                    field.busy = True
                    rabbit.state = "idle"
                    rabbit.hungry = False
                    rabbit.busy_field = field
                    rabbit.target_x = field.center_x
                    break

        for field in self.fields_list:
            # проверка съедания урожая
            if field.time_with_rabbit >= 5:
                # Если кролик на грядке более 5 секунд, добавляем укус
                field.quantity_bites += 1
                field.time_with_rabbit = 0
                self.garden_information.update_quantity_bites(
                    field.quantity_bites, field.number
                )
                if field.quantity_bites == 10:
                    # Если на грядке 10 укусов, растение пропадает
                    field.quantity_bites = 0
                    field.texture = self.empty_field_texture
                    field.rabbit.state = "run"
                    field.rabbit = None
                    self.garden_information.fields[field.number]["plant_name"] = None
                    self.garden_information.fields[field.number]["state"] = 0
                    self.garden_information.fields[field.number]["quantity_bites"] = 0
                    self.garden_information.save()
                    if field.number in self.plants_timers:
                        arcade.unschedule(self.plants_timers[field.number])
                        del self.plants_timers[field.number]

    def on_mouse_press(self, x, y, button, modifiers):
        # Проверка пересечения щелчка мыши со спрайтом семян для смены текстуры
        if self.seed.collides_with_point((x, y)):
            self.current_seed_texture = (self.current_seed_texture + 1) % 4
            self.seed.texture = self.seeds_textures[self.current_seed_texture]

        # Проверка пересечения щелчка мыши с грядками для изменения состояния
        for index, field_sprite in enumerate(self.fields_list):
            if field_sprite.collides_with_point((x, y)):
                self.planting_harvesting(field_sprite, index)

    def create_rabbit(self):
        """Метод создания кроликов"""
        rabbit = Rabbit()
        y_down1 = self.height - 0.1 * self.height - self.empty_field_texture.height + 10
        y_up1 = self.height - 0.1 * self.height - 10
        y_down2 = 0.1 * self.height + 10
        y_up2 = 0.1 * self.height + self.empty_field_texture.height - 10
        rabbit.center_y = random.choice(
            [
                random.randint(int(y_down1), int(y_up1)),
                random.randint(int(y_down2), int(y_up2)),
            ]
        )
        self.rabbits_list.append(rabbit)

    def choose_texture(self, sprite, field_number):
        """Метод выбора текстуры огорода по посаженному растению в бд"""
        field_information = self.garden_information.fields[field_number]
        plant = field_information["plant_name"]
        state = field_information["state"]
        if state == 0:
            sprite.texture = self.empty_field_texture
        elif state == 1:
            # Запуск таймера для автоматического роста семян, если пользователь вышел, не дождавшись
            arcade.schedule_once(
                lambda dt: self.update_plant_growth(sprite, field_number, plant),
                self.timers[plant],
            )
            sprite.texture = self.sprouts_field_texture
        elif state == 2:
            if plant == "Мандрагора":
                sprite.texture = self.mandragora_field_texture
            elif plant == "Белладонна":
                sprite.texture = self.belladonna_field_texture
            elif plant == "Красная роза":
                sprite.texture = self.rose_field_texture

    def planting_harvesting(self, sprite, field_number):
        """Метод проверки, что хочет сделать игрок при щелчке на грядку"""
        timer = None
        if self.seed.texture == self.shovel_texture:
            """Сбор урожая при возможности"""
            if self.garden_information.fields[field_number]["state"] == 2:
                if (
                    self.garden_information.fields[field_number]["plant_name"]
                    == "Мандрагора"
                ):
                    self.garden_information.quantity_mandragora += 1
                elif (
                    self.garden_information.fields[field_number]["plant_name"]
                    == "Белладонна"
                ):
                    self.garden_information.quantity_belladonna += 1
                elif (
                    self.garden_information.fields[field_number]["plant_name"]
                    == "Красная роза"
                ):
                    self.garden_information.quantity_rose += 1
                sprite.texture = self.empty_field_texture
                if sprite.rabbit:
                    # Если урожай собрали, кролик уходит
                    sprite.rabbit.state = "run"
                    sprite.rabbit = None
                self.garden_information.fields[field_number]["state"] = 0
                self.garden_information.fields[field_number]["plant_name"] = None
                self.garden_information.save()

                if self.garden_information.check_final():
                    self.window.switch_view("main_map")  # Показ финального окна
                return

        elif self.seed.texture == self.mandragora_seeds_texture:
            """Посадка мандрагоры при возможности и запуск таймера"""
            if (
                self.garden_information.fields[field_number]["state"] == 0
                and self.quantity_mandragora > 0
            ):
                self.quantity_mandragora -= 1
                self.garden_information.fields[field_number]["state"] = 1
                self.garden_information.fields[field_number][
                    "plant_name"
                ] = "Мандрагора"
                self.garden_information.quantity_mandragora_seeds = (
                    self.quantity_mandragora
                )
                sprite.texture = self.sprouts_field_texture
                self.garden_information.save()
                timer = arcade.schedule_once(
                    lambda dt: self.update_plant_growth(
                        sprite, field_number, "Мандрагора"
                    ),
                    self.timers["Мандрагора"],
                )

        elif self.seed.texture == self.belladonna_seeds_texture:
            """Посадка белладонны при возможности и запуск таймера"""
            if (
                self.garden_information.fields[field_number]["state"] == 0
                and self.quantity_belladonna > 0
            ):
                self.quantity_belladonna -= 1
                self.garden_information.fields[field_number]["state"] = 1
                self.garden_information.fields[field_number][
                    "plant_name"
                ] = "Белладонна"
                self.garden_information.quantity_belladonna_seeds = (
                    self.quantity_belladonna
                )
                sprite.texture = self.sprouts_field_texture
                self.garden_information.save()
                timer = arcade.schedule_once(
                    lambda dt: self.update_plant_growth(
                        sprite, field_number, "Белладонна"
                    ),
                    self.timers["Белладонна"],
                )

        elif self.seed.texture == self.rose_seeds_texture:
            """Посадка красной розы при возможности и запуск таймера"""
            if (
                self.garden_information.fields[field_number]["state"] == 0
                and self.quantity_rose > 0
            ):
                self.quantity_rose -= 1
                self.garden_information.fields[field_number]["state"] = 1
                self.garden_information.fields[field_number][
                    "plant_name"
                ] = "Красная роза"
                self.garden_information.quantity_rose_seeds = self.quantity_rose
                sprite.texture = self.sprouts_field_texture
                self.garden_information.save()
                timer = arcade.schedule_once(
                    lambda dt: self.update_plant_growth(
                        sprite, field_number, "Красная роза"
                    ),
                    self.timers["Красная роза"],
                )

        self.quantity_text.text = (
            f"Мандрагора - {self.quantity_mandragora}\n"
            f"Белладонна - {self.quantity_belladonna}\n"
            f"Красная роза - {self.quantity_rose}"
        )
        self.manager.trigger_render()  # Полная очистка менеджера для корректной отрисовки текста
        if timer:
            # Добавление таймеров
            self.plants_timers[field_number] = timer

    def update_plant_growth(self, sprite, field_number, plant_name):
        """Метод смены текстуры по истечению времени"""
        if self.garden_information.fields[field_number]["state"] == 0:
            # Если таймер установлен, но растение съели, не меняем текстуру
            return
        self.garden_information.fields[field_number]["state"] = 2
        if plant_name == "Мандрагора":
            sprite.texture = self.mandragora_field_texture
        elif plant_name == "Белладонна":
            sprite.texture = self.belladonna_field_texture
        elif plant_name == "Красная роза":
            sprite.texture = self.rose_field_texture
        self.garden_information.save()

    def exit(self):
        """Инициализация кнопки для перехода на представление главной карты"""
        x = self.width // 2 - self.exit_texture.width // 2
        y = self.height // 2 - self.exit_texture.height // 2
        button = UITextureButton(
            x=x,
            y=y,
            texture=self.exit_texture,
            texture_hovered=self.exit_texture,
            texture_pressed=self.exit_texture,
            scale=EXIT_SCALE,
        )

        @button.event("on_click")
        def on_click(event):
            self.window.switch_view("main_map")

        self.manager.add(button)

    def database_setting(self):
        """настройка данных из бд"""
        self.quantity_mandragora = self.garden_information.quantity_mandragora_seeds
        self.quantity_belladonna = self.garden_information.quantity_belladonna_seeds
        self.quantity_rose = self.garden_information.quantity_rose_seeds

    def on_show_view(self):
        """Активация ui менеджера и обновление данных из бд для синхронизации"""
        if self.manager:
            self.manager.enable()

        if self.garden_information:
            self.garden_information.update()
            self.database_setting()
            self.quantity_text.text = (
                f"Мандрагора - {self.quantity_mandragora}\n"
                f"Белладонна - {self.quantity_belladonna}\n"
                f"Красная роза - {self.quantity_rose}"
            )

    def on_hide_view(self):
        """Выключение ui менеджера"""
        if self.manager:
            self.manager.disable()
