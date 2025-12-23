from arcade.gui import UIInputText
import arcade

"""
Стиль для виджетов для ввода текста
"""

INPUT_TEXT_BG_COLOR = arcade.color.BLACK

input_text_style = {
    "normal": UIInputText.UIStyle(
        bg=INPUT_TEXT_BG_COLOR
    ),
    "hover": UIInputText.UIStyle(
        border=arcade.color.RED,
        bg=INPUT_TEXT_BG_COLOR
    ),
    "press": UIInputText.UIStyle(
        bg=INPUT_TEXT_BG_COLOR),
    "disabled": UIInputText.UIStyle(
        bg=INPUT_TEXT_BG_COLOR),
    "invalid": UIInputText.UIStyle(
        bg=INPUT_TEXT_BG_COLOR
    )
}