import arcade


class Cursor:
    def __init__(self, window):
        self.window = window
        self.window.set_mouse_visible(False)
        self.sprite = arcade.Sprite('resources/Cursor.png')
        self.x = None
        self.y = None