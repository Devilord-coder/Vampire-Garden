from arcade.gui import UIInputText
import arcade

"""
Стиль для виджетов для ввода текста
"""
input_text_style = {
    # You should provide a style for each widget state
    "normal": UIInputText.UIStyle(
        bg=arcade.color.BLACK
    ), # use default values for `normal` state
    "hover": UIInputText.UIStyle(
        border=arcade.color.RED,
        bg=arcade.color.BLACK
    ),
    "press": UIInputText.UIStyle(
        bg=arcade.color.BLACK),
    "disabled": UIInputText.UIStyle(
        bg=arcade.color.BLACK),
    "invalid": UIInputText.UIStyle(
        bg=arcade.color.BLACK
    )
}