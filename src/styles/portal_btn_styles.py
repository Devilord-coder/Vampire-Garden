import arcade
from arcade.gui import UIFlatButton


EASY_STYLE = {
    "normal": UIFlatButton.UIStyle(
        font_color=arcade.color.BLACK,
        bg=arcade.color.GREEN
    ),
    "hover": UIFlatButton.UIStyle(
        font_color=arcade.color.BLACK,
        bg=arcade.color.GREEN_YELLOW
    ),
    "press": UIFlatButton.UIStyle(
        font_color=arcade.color.BLACK,
        bg=arcade.color.GREEN_YELLOW
    ),
    "disabled": UIFlatButton.UIStyle(
        font_color=arcade.color.BLACK,
        bg=arcade.color.GREEN
    )
}

MEDIUM_STYLE = {
    "normal": UIFlatButton.UIStyle(
        font_color=arcade.color.BLACK,
        bg=arcade.color.YELLOW
    ),
    "hover": UIFlatButton.UIStyle(
        font_color=arcade.color.BLACK,
        bg=arcade.color.YELLOW_ORANGE
    ),
    "press": UIFlatButton.UIStyle(
        font_color=arcade.color.BLACK,
        bg=arcade.color.YELLOW_ORANGE
    ),
    "disabled": UIFlatButton.UIStyle(
        font_color=arcade.color.BLACK,
        bg=arcade.color.YELLOW
    )
}

HARD_STYLE = {
    "normal": UIFlatButton.UIStyle(
        font_color=arcade.color.BLACK,
        bg=arcade.color.RED
    ),
    "hover": UIFlatButton.UIStyle(
        font_color=arcade.color.BLACK,
        bg=arcade.color.RED_DEVIL
    ),
    "press": UIFlatButton.UIStyle(
        font_color=arcade.color.BLACK,
        bg=arcade.color.RED_DEVIL
    ),
    "disabled": UIFlatButton.UIStyle(
        font_color=arcade.color.BLACK,
        bg=arcade.color.RED
    )
}