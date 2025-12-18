from arcade.gui.widgets.buttons import UIFlatButton
import arcade

"""
Стиль для кнопок
"""
button_style = {
    "normal": UIFlatButton.UIStyle(
        font_color=arcade.color.AMARANTH,
        bg=arcade.color.BLACK
    ),
    "hover": UIFlatButton.UIStyle(
        font_color=arcade.color.RED,
        bg=arcade.color.BLACK,
    ),
    "press": UIFlatButton.UIStyle(
        font_color=arcade.color.RED,
        bg=arcade.color.BLACK
    ),
    "disabled": UIFlatButton.UIStyle(
        font_color=arcade.color.AMARANTH,
        bg=arcade.color.BLACK
    )
}