from arcade.gui import UIInputText
import arcade

"""
Стиль для виджетов для ввода текста
"""

bg_color = arcade.color.BLACK

input_text_style = {
    # You should provide a style for each widget state
    "normal": UIInputText.UIStyle(
        bg=bg_color
    ), # use default values for `normal` state
    "hover": UIInputText.UIStyle(
        border=arcade.color.RED,
        bg=bg_color
    ),
    "press": UIInputText.UIStyle(
        bg=bg_color),
    "disabled": UIInputText.UIStyle(
        bg=bg_color),
    "invalid": UIInputText.UIStyle(
        bg=bg_color
    )
}