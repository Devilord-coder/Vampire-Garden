import arcade
import arcade.gui
from src.creatures import Hero
from src.settings import settings
from src.registry import reg
from src.objects import Money

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
PLAYER_RUN_SPEED = 6

class BattleView(arcade.View):
    def __init__(self, window):
        super().__init__(window, background_color=arcade.color.BLACK)
        self.window = window

        # Здесь будут жить наши списки спрайтов из карты
        self.player_list = None
        self.hero = None
        self.physics_engine = None
        
        self.background = arcade.load_texture("resources/Background/dungeon_background.png")
        
        # Камеры: мир и GUI
        self.world_camera = arcade.camera.Camera2D()  # Камера для игрового мира
        self.gui_camera = arcade.camera.Camera2D()  # Камера для объектов интерфейса
        
        self.manager = arcade.gui.UIManager()

    def setup(self):
        """Настраиваем игру здесь. Вызывается при старте и при рестарте."""
        
        self.window.mouse.visible = False
        
        self.bg_sound = reg.battle_background_sound
        arcade.stop_sound(self.window.bg_sound_playback)
        self.bg_sound_playback = arcade.play_sound(self.bg_sound)
        
        # Инициализируем списки спрайтов
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()  # Сюда попадёт слой Collision!

        # ===== ВОЛШЕБСТВО ЗАГРУЗКИ КАРТЫ! (почти без магии). =====
        # Грузим тайловую карту
        map_name = MAP_TILE
        # Параметр 'scaling' ОЧЕНЬ важен! Умножает размер каждого тайла
        tile_map = arcade.load_tilemap(map_name, scaling=TILE_SCALING)

        # --- Достаём слои из карты как спрайт-листы ---
        self.wall_list = tile_map.sprite_lists["walls"]
        self.money_teritories_list = tile_map.object_lists["money"]
        self.money_init()
        self.enemies_territory_list = tile_map.object_lists["enemies"]
        self.enemy_init()
        self.exit_list = tile_map.sprite_lists["exit"]
        self.spikes_list = tile_map.sprite_lists["spikes"]
        self.spikes_collision = tile_map.sprite_lists["spikes_collision"]
        self.collision_list = self.wall_list
        for spike in self.spikes_list:
            self.collision_list.append(spike)
        for enemy in self.enemies_list:
            self.collision_list.append(enemy)
        
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
        
        # время игры
        self.main_time = 0
        
        # количество монеток
        self.money_count = {
            "gold": 0,
            "silver": 0,
            "bronze": 0
        }
        # картинки для монеток
        self.result_gold_money = arcade.load_texture("resources/Objects/money/gold/0.png")
        self.result_silver_money = arcade.load_texture("resources/Objects/money/silver/0.png")
        self.result_bronze_money = arcade.load_texture("resources/Objects/money/bronze/0.png")
        self.result_money_list = [self.result_gold_money,
                                  self.result_silver_money,
                                  self.result_bronze_money]
        self.health_pic = arcade.load_texture("resources/heart.png")
    
    def enemy_init(self):
        self.enemies_list = arcade.SpriteList()
        for enemy_ter in self.enemies_territory_list:
            enemy = ...
    
    def money_init(self):
        """ Инициализация монеток на карте """
        
        self.money_list = arcade.SpriteList()
        for money_territory in self.money_teritories_list:
            money = Money(type=money_territory.name)
            money.center_x = money_territory.shape[0]
            money.center_y = money_territory.shape[1]
            self.money_list.append(money)
    
    def on_show_view(self):
        """ Вызывается при показе этого представления """
        
        self.setup()

    def on_draw(self):
        """ Отрисовка экрана. """
        
        self.clear()
        
        # ------------- ЗАДНИЙ ФОН -------------
        arcade.draw_texture_rect(self.background, arcade.rect.XYWH(
            self.width // 2, self.height // 2,
            self.width, self.height
        ))

        # Отрисовка объектов
        self.world_camera.use()
        self.wall_list.draw()
        self.spikes_list.draw()
        self.exit_list.draw()
        self.money_list.draw()
        self.player_list.draw()
        
        # 2) GUI
        self.gui_camera.use()
        
        # ---- Количество денег ----
        # золотая монетка
        arcade.draw_texture_rect(
            self.result_gold_money,
            arcade.rect.XYWH(
                100, self.height - 50,
                50, 50
            )
        )
        # количество золота
        arcade.draw_text(
            str(self.money_count["gold"]),
            150, self.height - 60,
            arcade.color.RED,
            font_size=16
        )
        # серебрянная
        arcade.draw_texture_rect(
            self.result_silver_money,
            arcade.rect.XYWH(
                100, self.height - 120,
                50, 50
            )
        )
        # количество серебра
        arcade.draw_text(
            str(self.money_count["silver"]),
            150, self.height - 130,
            arcade.color.RED,
            font_size=16
        )
        # бронзовая
        arcade.draw_texture_rect(
            self.result_bronze_money,
            arcade.rect.XYWH(
                100, self.height - 190,
                50, 50
            )
        )
        # количество бронзы
        arcade.draw_text(
            str(self.money_count["bronze"]),
            150, self.height - 200,
            arcade.color.RED,
            font_size=16
        )
        
        arcade.draw_texture_rect(
            self.health_pic,
            arcade.rect.XYWH(250, self.height - 50,
                             50, 50)
        )
        arcade.draw_text(
            text=str(self.hero.health),
            x=275, y=self.height - 50,
            color=arcade.color.RED,
            font_size=15
        )
    
    def on_resize(self, width, height):
        """ Изменение размера окна """
        
        super().on_resize(width, height)
        self.setup()

    def on_update(self, delta_time):
        """ Обновление логики игры. """
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
        
        for money in self.money_list:
            money.update(delta_time)
            
        claim_money = arcade.check_for_collision_with_list(self.hero, self.money_list)
        for money in claim_money:
            self.money_count[money.type] += 1
            self.money_list.pop(self.money_list.index(money))
            arcade.play_sound(reg.money_claim_sound)
        
        hero_hurt = arcade.check_for_collision_with_list(self.hero, self.spikes_collision)
        if hero_hurt and not self.hero.hurting:
            self.hero.hurt(damage=20)
            print(self.hero.health)

        # Двигаем камеру за игроком (центрируем)
        # self.camera.move_to((self.player_sprite.center_x, self.player_sprite.center_y))

    def on_key_press(self, key, modifiers):
        """Обработка нажатий клавиш."""
        
        # Стандартное управление для PhysicsEngineSimple (как в уроке 2)
        if key == arcade.key.UP or key == arcade.key.W:
            self.hero.jump()
        elif key == arcade.key.LEFT or key == arcade.key.A:
            if modifiers in {arcade.key.MOD_COMMAND, arcade.key.MOD_CTRL}:
                self.hero.run_back()
            else:
                self.hero.walk_back()
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            if modifiers in {arcade.key.MOD_COMMAND, arcade.key.MOD_CTRL}:
                self.hero.run_forward()
            else:
                self.hero.walk_forward()
        elif key in {arcade.key.A, arcade.key.DOWN}:
            self.hero.down()
        elif key == arcade.key.SPACE:
            self.hero.attack()
        elif key == arcade.key.B and modifiers in {arcade.key.MOD_COMMAND, arcade.key.MOD_CTRL}:
            self.hero.transform()
        elif key == arcade.key.ESCAPE:
            arcade.stop_sound(self.bg_sound_playback)
            self.window.bg_sound_playback = arcade.play_sound(self.window.bg_sound)
            self.window.mouse.visible = True
            self.manager.disable()
            self.window.switch_view("main_map")
        elif key == arcade.key.P and modifiers in {arcade.key.MOD_COMMAND, arcade.key.MOD_CTRL}:
            self.hero.hurt(damage=20)
        elif key == arcade.key.R and modifiers in {arcade.key.MOD_COMMAND, arcade.key.MOD_CTRL}:
            self.setup()

    def on_key_release(self, key, modifiers):
        """ Обработка отпускания клавиш """
        
        if key in (arcade.key.UP, arcade.key.DOWN, arcade.key.W, arcade.key.S):
            self.hero.change_y = 0
        elif key in (arcade.key.LEFT, arcade.key.RIGHT, arcade.key.A, arcade.key.D):
            self.hero.change_x = 0
