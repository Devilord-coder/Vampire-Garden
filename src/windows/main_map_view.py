import arcade
from pyglet.graphics import Batch
from src.settings import settings
from src.auxiliary_classes.portal_animated_button import AnimatedPortalButton
import arcade.gui

TILE_SCALING = 1


class MainMapView(arcade.View):
    """Вид создания основной карты игры"""

    def __init__(self, window):
        super().__init__()
        arcade.set_background_color(arcade.color.ANTIQUE_RUBY)
        self.buildings = {
            "library": "resources/Buildings/library.png",
            "bat_house": "resources/Buildings/bat_house.png",
            "main_house": "resources/Buildings/main_house.png",
            "sport_hall": "resources/Buildings/sport_hall.png",
            "sceleton_house": "resources/Buildings/sceleton_house.png",
            "portal": "resources/Portal/portal1.png",
            "vampire_house": "resources/Buildings/vampire_house.png",
            "werewolf_house": "resources/Buildings/werewolf_house.png",
            "garden": "resources/Buildings/garden.jpg",
        }
        self.window = window
        self.batch = Batch()
        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()
        self.setup()

    def setup(self):
        # Загрузка карты
        self.tilemap = arcade.load_tilemap("maps/main_map.tmx", TILE_SCALING)

        self.background_list = self.tilemap.sprite_lists["background"]
        self.path_list = self.tilemap.sprite_lists["path"]
        self.collisions_list = self.tilemap.sprite_lists["collisions"]

        self.buildings_territories = None
        for layer_name, sprite_list in self.tilemap.object_lists.items():
            if layer_name == "buildings_territories":
                self.buildings_territories = sprite_list
                break

        self.center_map()
        self.buttons_init()

    def buttons_init(self):
        # Инициализация всех кнопок зданий
        for building in self.buildings_territories:
            building_name = building.name
            image_path = self.buildings[building_name]

            if building_name == "portal":
                texture_list = []
                for i in range(1, 5):
                    texture = arcade.load_texture(f"resources/Portal/portal{i}.png")
                    texture_list.append(texture)

                button = AnimatedPortalButton(
                    x=building.shape[3][0],
                    y=building.shape[3][1],
                    texture_list=texture_list,
                    scale=1.0,
                )

            else:
                texture = arcade.load_texture(image_path)

                button = arcade.gui.UITextureButton(
                    x=building.shape[3][0],
                    y=building.shape[3][1],
                    texture=texture,
                    texture_hovered=texture,
                    texture_pressed=texture,
                    scale=1.0,
                )
            button.building_name = building_name

            @button.event("on_click")
            def on_click(event):
                # Обработка клика по кнопке (перемещение на следующие виды игры для каждого здания)
                building_name = event.source.building_name
                if building_name == "main_house":
                    print("Главное здание")
                elif building_name == "library":
                    print("Библиотека")
                elif building_name == "bat_house":
                    print("Дом летучих мышей")
                elif building_name == "sport_hall":
                    print("Спортзал")
                elif building_name == "garden":
                    print("Огород")
                elif building_name == "portal":
                    print("Портал")
                elif building_name == "vampire_house":
                    print("Дом вампиров")
                elif building_name == "werewolf_house":
                    print("Дом оборотней")
                elif building_name == "sceleton_house":
                    print("Дом скелетов")

            self.ui_manager.add(button)

    def center_map(self):
        # Центрирование карты относительно окна
        window_width, window_height = self.window.get_size()

        map_width = self.tilemap.width * self.tilemap.tile_width
        map_height = self.tilemap.height * self.tilemap.tile_height

        offset_x = (window_width - map_width) / 2
        offset_y = (window_height - map_height) / 2

        for sprite_list in [self.background_list, self.path_list, self.collisions_list]:
            for sprite in sprite_list:
                sprite.center_x += offset_x
                sprite.center_y += offset_y

        if self.buildings_territories:
            for building in self.buildings_territories:
                for pos in range(4):
                    x, y = building.shape[pos]
                    x += offset_x
                    y += offset_y
                    building.shape[pos] = (x, y)

    def on_draw(self):
        self.clear()
        self.background_list.draw()
        self.path_list.draw()
        self.ui_manager.draw()

    def on_update(self, delta_time):
        # Обновление кнопок и анимации кнопки портала
        self.ui_manager.on_update(delta_time)
        for widget in self.ui_manager.children:
            if hasattr(widget, "child") and widget.child is not None:
                if isinstance(widget.child, AnimatedPortalButton):
                    widget.child.on_update(delta_time)
