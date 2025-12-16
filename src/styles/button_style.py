from arcade.gui.widgets.buttons import UIFlatButton
import arcade

"""
Стиль для кнопок
"""
button_style = {
    # You should provide a style for each widget state
    "normal": UIFlatButton.UIStyle(
        font_color=arcade.color.RED,
        bg=arcade.color.BLACK
    ), # use default values for `normal` state
    "hover": UIFlatButton.UIStyle(
        font_color=arcade.color.AMARANTH_PURPLE,
        bg=arcade.color.BLACK_BEAN,
    ),
    "press": UIFlatButton.UIStyle(
        font_color=arcade.color.RED,
        bg=arcade.color.BLACK
    ),
    "disabled": UIFlatButton.UIStyle(
        font_color=arcade.color.RED,
        bg=arcade.color.BLACK
    )
}