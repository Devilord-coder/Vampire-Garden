import arcade
import arcade.gui


class WinBattleView(arcade.View):
    def __init__(self, window):
        super().__init__()
        
        self.window = window
    
    def setup(self):
        pass
    
    def on_show_view(self):
        self.setup()
    
    def on_draw(self):
        ...
    
    def on_update(self, delta_time):
        ...