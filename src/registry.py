import arcade
from os import listdir


class Registry:
    def __init__(self):
        # голос вампира из предыстории
        self.prehistory_voice = arcade.load_sound(
            "resources/sounds/prehistory_sound.wav"
        )
        # задний фон
        self.background_sound = arcade.load_sound(
            "resources/sounds/background_sound.wav"
        )
        # нажатие кнопки
        self.button_click_sound = arcade.load_sound("resources/sounds/button_click.wav")

        self.door_sound = arcade.load_sound("resources/sounds/door.mp3")
        self.buy_sound = arcade.load_sound("resources/sounds/buy.mp3")
        self.book_sound = arcade.load_sound("resources/sounds/book.mp3")
        self.harvesting_mandragora_sound = arcade.load_sound(
            "resources/sounds/mandragora.mp3"
        )
        self.plants_sound = arcade.load_sound("resources/sounds/plants.mp3")
        self.sad_sound = arcade.load_sound("resources/sounds/sad.mp3")

        self.tutorial_sounds = []  # Звуки для туториала
        for i in range(8):
            sound = arcade.load_sound(f"resources/tutorial/audios/audio{i}.mp3")
            self.tutorial_sounds.append(sound)

        # захват монетки
        self.money_claim_sound = arcade.load_sound("resources/sounds/claim_money.wav")
        # задний фон битвы
        self.battle_background_sound = arcade.load_sound(
            "resources/sounds/battle_background_sound.wav"
        )

        # инициализация текктур для огненного шара
        self.fireboll_textures_init()

        ...

    def fireboll_textures_init(self):
        """Инициализация текстур огненного шара"""

        self.fireboll_fly_textures = []
        self.fireboll_attack_textures = []
        self.fireboll_reverse_fly_textures = []

        for file_name in filter(
            lambda x: x[-4:] == ".png",  # выбор всех картинок (.png) из нужной папки
            listdir("resources/Objects/fireboll/fly"),
        ):
            self.fireboll_fly_textures.append(
                arcade.load_texture(f"resources/Objects/fireboll/fly/{file_name}")
            )

        for file_name in filter(
            lambda x: x[-4:] == ".png", listdir("resources/Objects/fireboll/attack")
        ):
            self.fireboll_attack_textures.append(
                arcade.load_texture(f"resources/Objects/fireboll/attack/{file_name}")
            )
        
        for file_name in filter(
            lambda x: x[-4:] == ".png", listdir("resources/Objects/fireboll/reverse_fly")
        ):
            self.fireboll_reverse_fly_textures.append(
                arcade.load_texture(f"resources/Objects/fireboll/reverse_fly/{file_name}")
            )


reg = Registry()
