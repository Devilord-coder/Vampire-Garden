from arcade.gui import UIInputText
import arcade

"""
Стиль для виджетов для ввода текста
"""

bg_color = arcade.color.BLACK

input_text_style = {
    "normal": UIInputText.UIStyle(
        bg=bg_color
    ),
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