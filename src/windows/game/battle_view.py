import arcade
from src.Creatures import Hero
from src.settings import settings

SCREEN_WIDTH = settings.width
SCREEN_HEIGHT = settings.height

SCREEN_TITLE = "Level 1"
TILE_SCALING = 1  # Если тайлы 64x64, а хотим чтобы на экране были 64x64 — ставим 1.0
MAP_TILE = "maps/example_map.tmx"  # тайл карты

# Физика и движение
GRAVITY = 0.5           # Пикс/с^2

# Качество жизни прыжка
COYOTE_TIME = 0.08        # Сколько после схода с платформы можно ещё прыгнуть
JUMP_BUFFER = 0.12        # Если нажали прыжок чуть раньше приземления, мы его «запомним» (тоже лайфхак для улучшения качества жизни игрока)
MAX_JUMPS = 1             # С двойным прыжком всё лучше, но не сегодня

# ---------- Камера ----------
CAMERA_LERP = 0.12
DEAD_ZONE_W = int(SCREEN_WIDTH * 0.35)
DEAD_ZONE_H = int(SCREEN_HEIGHT * 0.45)

# --------- Персонаж ---------
PLAYER_SCALING = 1.2
PLAYER_JUMP_SPEED = 10
PLAYER_WALK_SPEED = 3
PLAYER_RUN_SPEED = 5

class BattleView(arcade.View):
    def __init__(self, window):
        super().__init__(window, background_color=arcade.color.BLACK)
        self.window = window

        # Здесь будут жить наши списки спрайтов из карты
        self.wall_list = None
        self.player_list = None
        self.hero = None
        self.physics_engine = None
        
        self.background = arcade.load_texture("resources/Background/dungeon_background.png")
        
        # Камеры: мир и GUI
        self.world_camera = arcade.camera.Camera2D()  # Камера для игрового мира
        self.gui_camera = arcade.camera.Camera2D()  # Камера для объектов интерфейса

    def setup(self):
        """Настраиваем игру здесь. Вызывается при старте и при рестарте."""
        # Инициализируем списки спрайтов
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()  # Сюда попадёт слой Collision!

        # ===== ВОЛШЕБСТВО ЗАГРУЗКИ КАРТЫ! (почти без магии). =====
        # Грузим тайловую карту
        map_name = MAP_TILE
        # Параметр 'scaling' ОЧЕНЬ важен! Умножает размер каждого тайла
        tile_map = arcade.load_tilemap(map_name, scaling=TILE_SCALING)

        # --- Достаём слои из карты как спрайт-листы ---
        self.flat_list = tile_map.sprite_lists["flat"]
        self.collision_list = self.flat_list
        # --- Создаём игрока. ---
        # Карту загрузили, теперь создаём героя, который будет по ней бегать
        self.hero = Hero(
            PLAYER_SCALING,
            PLAYER_WALK_SPEED,
            PLAYER_RUN_SPEED,
            PLAYER_JUMP_SPEED
        )
        # Ставим игрока куда-нибудь на землю (посмотрите в Tiled, где у вас земля!)
        self.hero.center_x = 100  # Примерные координаты
        self.hero.center_y = 300  # Примерные координаты
        self.player_list.append(self.hero)

        # --- Физический движок ---
        # Используем PhysicsEngineSimple, который знаем и любим
        # Он даст нам движение и коллизии со стенами (self.wall_list)!
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.hero,
            gravity_constant=GRAVITY,
            walls=self.collision_list
        )
        self.physics_engine_bat = arcade.PhysicsEngineSimple(
            self.hero, self.collision_list
        )
        
        # Сбросим вспомогательные таймеры
        self.jump_buffer_timer = 0
        self.time_since_ground = 999.0
        self.jumps_left = MAX_JUMPS
        
        self.main_time = 0
    
    def on_show_view(self):
        self.setup()

    def on_draw(self):
        """ Отрисовка экрана. """
        
        self.clear()
        
        # ------------- ЗАДНИЙ ФОН -------------
        arcade.draw_texture_rect(self.background, arcade.rect.XYWH(
            self.width // 2, self.height // 2,
            self.width, self.height
        ))

        self.world_camera.use()
        self.flat_list.draw()
        self.player_list.draw()
        
        # 2) GUI
        self.gui_camera.use()

        # self.collision_list.draw()  # Обычно НЕ рисуем слой коллизий в финальной игре, но для отладки бывает полезно
    
    def on_resize(self, width, height):
        """ Изменение размера окна """
        
        super().on_resize(width, height)
        self.setup()

    def on_update(self, delta_time):
        """Обновление логики игры."""
        # Обновляем физический движок (двигает игрока и проверяет стены)
        if not self.hero.bat:
            self.physics_engine.update()
        else:
            self.physics_engine_bat.update()
            
        position = (
            self.hero.center_x,
            self.hero.center_y
        )
        self.world_camera.position = arcade.math.lerp_2d(
            self.world_camera.position,
            position,
            CAMERA_LERP  # Плавность следования камеры
        )
        
        self.hero.update(delta_time)

        # Двигаем камеру за игроком (центрируем)
        # self.camera.move_to((self.player_sprite.center_x, self.player_sprite.center_y))

    def on_key_press(self, key, modifiers):
        """Обработка нажатий клавиш."""
        
        # Стандартное управление для PhysicsEngineSimple (как в уроке 2)
        if key == arcade.key.UP or key == arcade.key.W:
            self.hero.jump()
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.hero.walk_back()
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.hero.walk_forward()
        elif key in {arcade.key.A, arcade.key.DOWN}:
            self.hero.down()
        elif key == arcade.key.B and modifiers in {arcade.key.MOD_COMMAND, arcade.key.MOD_CTRL}:
            self.hero.transform()

    def on_key_release(self, key, modifiers):
        """Обработка отпускания клавиш."""
        if key in (arcade.key.UP, arcade.key.DOWN, arcade.key.W, arcade.key.S):
            self.hero.change_y = 0
        elif key in (arcade.key.LEFT, arcade.key.RIGHT, arcade.key.A, arcade.key.D):
            self.hero.change_x = 0
