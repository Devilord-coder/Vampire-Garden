import arcade


class Registry:
    def __init__(self):
        # голос вампира из предыстории
        self.prehistory_voice = arcade.load_sound("resources/sounds/prehistory_sound.wav")
        # задний фон
        self.background_sound = arcade.load_sound("resources/sounds/background_sound.wav")
        # нажатие кнопки
        self.button_click_sound = arcade.load_sound("resources/sounds/button_click.wav")
        # захват монетки
        self.money_claim_sound = arcade.load_sound("resources/sounds/claim_money.wav")
        # задний фон битвы
        self.battle_background_sound = arcade.load_sound("resources/sounds/battle_background_sound.wav")
        
        ...
    

reg = Registry()
