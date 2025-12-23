import arcade
import arcade.gui


class AnimatedPortalButton(arcade.gui.UITextureButton):
    """Анимированная кнопка для портала"""

    def __init__(self, x, y, texture_list, scale=1.0):
        super().__init__(x=x, y=y, texture=texture_list[0], scale=scale)
        self.texture_list = texture_list
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_delay = 0.2

    def on_update(self, delta_time):
        # Смена текстур кнопки с течением времени
        self.frame_timer += delta_time
        if self.frame_timer >= self.frame_delay:
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.texture_list)
            self.texture = self.texture_list[self.current_frame]