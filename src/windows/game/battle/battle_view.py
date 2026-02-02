import arcade
import arcade.gui
from src.creatures import Hero, ENEMIES, ENEMIES_PRICE
from .battle_physics import *
from src.registry import reg
from src.objects import Money


class BattleView(arcade.View):
    """ Главное коно битвы """
    
    def __init__(self, window):
        super().__init__(window, background_color=arcade.color.BLACK)
        self.window = window

        # Здесь будут жить наши списки спрайтов из карты
        self.player_list = None
        self.hero = None
        self.physics_engine = None
        
        self.background = arcade.load_texture("resources/Background/dungeon_background.png")
        self.bg_sound = reg.battle_background_sound
        self.bg_sound_playback = None
        
        # Камеры: мир и GUI
        self.world_camera = arcade.camera.Camera2D()  # Камера для игрового мира
        self.gui_camera = arcade.camera.Camera2D()  # Камера для объектов интерфейса
        
        self.manager = arcade.gui.UIManager()
        
        self.map_name = None
        
        self.enemies_killed_names = []
        
        self.setup()

    def setup(self):
        """ Настраиваем игру здесь. Вызывается при старте и при рестарте. """
        
        if not self.map_name:
            return
        
        self.window.mouse.visible = False
        self.manager.enable()
        
        arcade.stop_sound(self.window.bg_sound_playback)
        if self.bg_sound_playback:
            arcade.stop_sound(self.bg_sound_playback)
        self.bg_sound_playback = arcade.play_sound(self.bg_sound, loop=True)
        
        # Инициализируем списки спрайтов
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()  # Сюда попадёт слой Collision!
        self.firebolls_list = arcade.SpriteList()

        # ===== ВОЛШЕБСТВО ЗАГРУЗКИ КАРТЫ! (почти без магии). =====
        # Параметр 'scaling' ОЧЕНЬ важен! Умножает размер каждого тайла
        tile_map = arcade.load_tilemap(self.map_name, scaling=TILE_SCALING)

        # --- Достаём слои из карты как спрайт-листы ---
        self.wall_list = tile_map.sprite_lists["walls"]
        self.money_teritories_list = tile_map.object_lists["money"]
        self.money_init()
        self.enemies_territory_list = tile_map.object_lists["enemies"]
        self.exit_list = tile_map.sprite_lists["exit"]
        self.spikes_list = tile_map.sprite_lists["spikes"]
        self.spikes_collision = tile_map.sprite_lists["spikes_collision"]
        self.secret_list = tile_map.sprite_lists["secret"]
        self.collision_list = self.wall_list
        self.enemy_init()
        self.enemies_count = len(self.enemies_list) # количество врагов
        self.enemies_killed = 0 # количество убитых врагов
        for spike in self.spikes_list:
            self.collision_list.append(spike)
        
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
        self.hero.center_y = 200  # Примерные координаты
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
        # время после смерти
        self.time_after_death = 0
        
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
        """ Инициализация всех врагов """
        
        self.enemies_list = arcade.SpriteList()
        self.enemies_engine_list = []
        for enemy_ter in self.enemies_territory_list:
            enemy = ENEMIES[enemy_ter.name](walk_speed=0.5, scaling=0.75, enemies_name_list=self.enemies_killed_names)
            x, y = enemy_ter.shape[0], enemy_ter.shape[1]
            enemy.center_x = x
            enemy.center_y = y
            enemy.boundary_left = x - 40
            enemy.boundary_right = x + 40
            enemy_engine = self.physics_engine = arcade.PhysicsEnginePlatformer(
            player_sprite=enemy,
            gravity_constant=GRAVITY,
            walls=self.collision_list
            )
            self.enemies_engine_list.append(enemy_engine)
            self.enemies_list.append(enemy)
            
            
    
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
        
        if not self.map_name:
            return
        
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
        self.enemies_list.draw()
        self.secret_list.draw()
        self.firebolls_list.draw()
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
        # отрисовка сердечка
        arcade.draw_texture_rect(
            self.health_pic,
            arcade.rect.XYWH(250, self.height - 50,
                             50, 50)
        )
        # отрисовка количесвта жизней
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
    
    def set_map(self, map_name):
        self.map_name = f"maps/{map_name}"
        self.setup()

    def on_update(self, delta_time):
        """ Обновление логики игры. """
        
        if not self.map_name:
            return
        
        if not self.hero:
            return
        
        # Обновляем физический движок (двигает игрока и проверяет стены)
        if not self.hero.bat:
            self.physics_engine.update()
        else:
            self.physics_engine_bat.update()
        
        if self.enemies_count != len(self.enemies_list):
            self.enemies_killed += self.enemies_count - len(self.enemies_list)
            self.enemies_count = len(self.enemies_list)
        
        for engine in self.enemies_engine_list:
            engine.update()
        
        for enemy in self.enemies_list:
            enemy.update(delta_time)
        
        for boll in self.firebolls_list:
            if boll.deleted:
                self.firebolls_list.pop(self.firebolls_list.index(boll))
            else:
                boll.update(delta_time)
            
        position = (
            self.hero.center_x,
            self.hero.center_y
        )
        self.world_camera.position = arcade.math.lerp_2d(
            self.world_camera.position,
            position,
            CAMERA_LERP  # Плавность следования камеры
        )
        # обновление персонажа
        self.hero.update(delta_time)

        if self.hero.dead:
            self.time_after_death += delta_time
        # проверка смерти персонажа
        if self.time_after_death >= 1.5:
            self.end_game()
        
        is_exit = arcade.check_for_collision_with_list(self.hero, self.exit_list)
        if is_exit:
            self.win_game()
        
        # обновление монеток
        for money in self.money_list:
            money.update(delta_time)
            
        # проверка получения монеток
        claim_money = arcade.check_for_collision_with_list(self.hero, self.money_list)
        if not self.hero.bat:
            for money in claim_money:
                self.money_count[money.type] += 1
                self.money_list.pop(self.money_list.index(money))
                arcade.play_sound(reg.money_claim_sound)
        
        # проверка получения урона
        hero_hurt = arcade.check_for_collision_with_list(self.hero, self.spikes_collision)
        if hero_hurt and not self.hero.hurting:
            self.hero.hurt(damage=20)
        
        # проверка на столкновение игрорка с врагами
        if not self.hero.hurting:
            enemies_attack = arcade.check_for_collision_with_list(self.hero, self.enemies_list)
            for enemy in enemies_attack:
                self.hero.hurt(enemy.power)
                enemy.attack()

        # Двигаем камеру за игроком (центрируем)
        # self.camera.move_to((self.hero.center_x, self.hero.center_y))
    
    def end_game(self):
        """ Окончание игры при смерти персонажа """
        
        arcade.stop_sound(self.bg_sound_playback)
        self.window.bg_sound_playback = arcade.play_sound(self.window.bg_sound, loop=True)
        self.window.mouse.visible = True
        self.manager.disable()
        battle_statistic_view = self.window.get_view("battle_statistic")
        battle_statistic_view.gold = self.money_count["gold"]
        battle_statistic_view.silver = self.money_count["silver"]
        battle_statistic_view.bronze = self.money_count["bronze"]
        battle_statistic_view.enemies = self.enemies_killed
        self.window.switch_view("battle_statistic")
    
    def win_game(self):
        """ Окончание игры при победе """
        
        arcade.stop_sound(self.bg_sound_playback)
        self.window.bg_sound_playback = arcade.play_sound(self.window.bg_sound, loop=True)
        self.window.mouse.visible = True
        self.manager.disable()
        battle_statistic_view = self.window.get_view("win_battle_view")
        battle_statistic_view.gold = self.money_count["gold"]
        battle_statistic_view.silver = self.money_count["silver"]
        battle_statistic_view.bronze = self.money_count["bronze"]
        battle_statistic_view.enemies = self.enemies_killed
        battle_statistic_view.enemies_money = sum(map(lambda x: ENEMIES_PRICE[x], self.enemies_killed_names))
        self.window.switch_view("win_battle_view")

    def on_key_press(self, key, modifiers):
        """Обработка нажатий клавиш."""
        
        if not self.hero:
            return
        
        if key == arcade.key.UP:
            self.hero.jump()
        elif key == arcade.key.LEFT:
            if modifiers in {arcade.key.MOD_COMMAND, arcade.key.MOD_CTRL}:
                self.hero.run_back()
            else:
                self.hero.walk_back()
        elif key == arcade.key.RIGHT:
            if modifiers in {arcade.key.MOD_COMMAND, arcade.key.MOD_CTRL}:
                self.hero.run_forward()
            else:
                self.hero.walk_forward()
        elif key == arcade.key.DOWN:
            self.hero.down()
        elif key == arcade.key.D:
            sx = 3
            if self.hero.change_y > 0:
                 sy = 2
            elif self.hero.change_y < 0:
                sy = -2
            else:
                sy = 0
            
            # атака героя -> возвращает огненный шар
            fireboll = self.hero.attack(
                'f',
                (self.hero.center_x, self.hero.center_y), # передаем координаты
                (sx, sy), # скорость по х и у
                [self.wall_list], # стены
                [self.enemies_list] # враги
            )
            # добавляем огненный шар
            self.firebolls_list.append(fireboll)
        elif key == arcade.key.A:
            sx = -3
            if self.hero.change_y > 0:
                 sy = 2
            elif self.hero.change_y < 0:
                sy = -2
            else:
                sy = 0
            
            # атака героя -> возвращает огненный шар
            fireboll = self.hero.attack(
                'r',
                (self.hero.center_x, self.hero.center_y), # передаем координаты
                (sx, sy), # скорость по х и у
                [self.wall_list], # стены
                [self.enemies_list] # враги
            )
            # добавляем огненный шар
            self.firebolls_list.append(fireboll)
        elif key == arcade.key.B and modifiers in {arcade.key.MOD_COMMAND, arcade.key.MOD_CTRL}:
            self.hero.transform()
        elif key == arcade.key.ESCAPE:
            arcade.stop_sound(self.bg_sound_playback)
            self.window.bg_sound_playback = arcade.play_sound(self.window.bg_sound, loop=True)
            self.window.mouse.visible = True
            self.manager.disable()
            self.window.switch_view("main_map")
        elif key == arcade.key.P and modifiers in {arcade.key.MOD_COMMAND, arcade.key.MOD_CTRL}:
            self.hero.hurt(damage=20)
        elif key == arcade.key.R and modifiers in {arcade.key.MOD_COMMAND, arcade.key.MOD_CTRL}:
            self.setup()

    def on_key_release(self, key, modifiers):
        """ Обработка отпускания клавиш """
        
        if not self.hero:
            return
        
        if key in (arcade.key.UP, arcade.key.DOWN, arcade.key.W, arcade.key.S):
            self.hero.change_y = 0
        elif key in (arcade.key.LEFT, arcade.key.RIGHT, arcade.key.A, arcade.key.D):
            self.hero.change_x = 0
