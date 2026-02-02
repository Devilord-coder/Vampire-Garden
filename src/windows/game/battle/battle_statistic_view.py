from src.styles import *

import arcade
import arcade.gui
from arcade.gui import UILabel, UIManager
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout


class BattleStatisticView(arcade.View):
    """ Окно для показа статистики и результатов боя """
    
    def __init__(self, window):
        super().__init__()
        
        self.window = window
        
        # Важно не вызывать setup при инициализации, так как часть параметров передаются вручную позже 
        # то есть setup вызывается только при показе представления
    
    def setup(self):
        """ Настройка представления """
        arcade.set_background_color(arcade.color.BLACK)
        
        # UIManager — сердце GUI
        self.manager = UIManager()
        self.manager.enable()  # Включить, чтоб виджеты работали
        
        # Layout для организации — как полки в шкафу
        self.anchor_layout = UIAnchorLayout()  # Центрирует виджеты
        self.box_layout = UIBoxLayout(vertical=True, space_between=20)  # Вертикальный стек
        
        game_over_text = UILabel(
            text="GAME OVER",
            text_color=TEXT_COLOR,
            font_size=30,
            multiline=True
        )
        
        # количество золота
        gold_text = UILabel(
            text=f"GOLD - {self.gold}",
            text_color=TEXT_COLOR,
            font_size=18,
            multiline=True,
            align="left"
        )
        
        # количество серербра
        silver_text = UILabel(
            text=f"SILVER - {self.silver}",
            text_color=TEXT_COLOR,
            font_size=18,
            multiline=True,
            align="left"
            
        )
        
        # количество бронзы
        bronze_text = UILabel(
            text=f"BRONZE - {self.bronze}",
            text_color=TEXT_COLOR,
            font_size=18,
            multiline=True,
            align="left"
        )
        
        # количество убитых врагов
        enemies_text = UILabel(
            text=f"ENEMIES - {self.enemies}",
            text_color=TEXT_COLOR,
            font_size=18,
            multiline=True,
            align="left"
        )
        
        # ==== ДОБАВЛЯЕМ ВИДЖЕТЫ ПО ПОРЯДКУ ====
        self.box_layout.add(game_over_text)
        self.box_layout.add(gold_text)
        self.box_layout.add(silver_text)
        self.box_layout.add(bronze_text)
        self.box_layout.add(enemies_text)
        
        self.anchor_layout.add(self.box_layout)  # Box в anchor
        self.manager.add(self.anchor_layout)  # Всё в manager
        
        # чтобы мигало сообщение о продолжении игры
        self.time_between_restarting_message = 0
        self.draw_restart_message = True
    
    def on_show_view(self):
        """ Вызов представления """
        
        self.setup()
    
    def on_draw(self):
        """ Отрисовка """
        
        self.clear()
        
        self.manager.draw()
        
        arcade.draw_text(
            text="TAP TO RESTART",
            x=self.width // 2 - 60,
            y=300,
            color=arcade.color.WHITE_SMOKE
        )
    
    def on_update(self, delta_time):
        """ Обновление логики пердставления """
        
        self.time_between_restarting_message += 1
        if self.time_between_restarting_message >= 1.5:
            if self.draw_restart_message:
                self.draw_restart_message = False
            else:
                self.draw_restart_message = True
            self.time_between_restarting_message = 0
    
    def on_mouse_press(self, x, y, button, modifiers):
        self.manager.disable()
        self.window.switch_view("battle")
    
    def on_key_press(self, key, modifiers):
        """ Нажатие клавиш """
        
        if key == arcade.key.R and modifiers in {arcade.key.MOD_COMMAND, arcade.key.MOD_CTRL}:
            self.manager.disable()
            self.window.switch_view("battle")