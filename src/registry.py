import arcade


class Registry:
    def __init__(self):
        # голос вампира из предыстории
        self.prehistory_voice = arcade.load_sound("resources/sounds/prehistory_sound.wav")
        self.background_sound = arcade.load_sound("resources/sounds/background_sound.wav")
        self.button_click_sound = arcade.load_sound("resources/sounds/button_click.wav")
        self.door_sound = arcade.load_sound('resources/sounds/door.mp3')
        self.buy_sound = arcade.load_sound('resources/sounds/buy.mp3')
        self.book_sound = arcade.load_sound('resources/sounds/book.mp3')
        self.harvesting_mandragora_sound = arcade.load_sound('resources/sounds/mandragora.mp3')
        self.plants_sound = arcade.load_sound('resources/sounds/plants.mp3')
        ...
    

reg = Registry()
