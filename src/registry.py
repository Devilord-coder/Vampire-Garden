import arcade


class Registry:
    def __init__(self):
        # голос вампира из предыстории
        self.prehistory_voice = arcade.load_sound("resources/sounds/prehistory_sound.wav")
        self.background_sound = arcade.load_sound("resources/sounds/background_sound.wav")
        self.button_click_sound = arcade.load_sound("resources/sounds/button_click.wav")
        
        ...
    

reg = Registry()
