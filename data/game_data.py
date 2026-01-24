import sqlite3


class GameData:
    """Класс для работы с бд для отслеживания состояния игры в целом"""

    def __init__(self, window):
        self.window = window
        self.con = self.window.con
        self.cur = self.con.cursor()
        self.game_number = self.window.game_number
        self.login = None
        self.game_id = None
        self.garden_id = None

    def get_user_id(self):
        """Метод получения id пользователя по логину"""

        self.login = self.window.login
        id = self.cur.execute(
            "SELECT id FROM Registry WHERE login=?", (self.login,)
        ).fetchone()
        return id[0]

    def get_game_state(self):
        """Метод получения id игры (ели игры ещё не было, создаём новую)"""

        self.login = self.window.login
        res = self.cur.execute(
            """SELECT Game.id, quantity_money FROM Game
                                  JOIN Registry on Game.user_id=Registry.id
                                  WHERE Game.game_number=? AND Registry.login=?""",
            (self.game_number, self.login),
        ).fetchone()
        if res:
            self.game_id = res[0]
            self.window.game_id = self.game_id
            self.window.quantity_money = res[1]
            self.get_garden_id()
            return True  # Игра уже была

        user_id = self.get_user_id()
        self.cur.execute(
            """INSERT INTO Game(user_id, game_number, quantity_money, quantity_mandragora_seeds,
            quantity_belladonna_seeds, quantity_rose_seeds, quantity_mandragora, quantity_belladonna, quantity_rose,
            quantity_bats, quantity_sceletons, quantity_werewolves,
            quantity_planted_mandragora, quantity_planted_belladonna, quantity_planted_rose)
            VALUES(?, ?, 500, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)""",
            (user_id, self.game_number),
        )  # Создание данных для новой игры (изначально 500 монет)
        self.con.commit()
        res = self.cur.lastrowid
        self.game_id = res
        self.window.game_id = res
        self.window.quantity_money = 0
        self.create_new_garden()
        return False  # Создана новая игра

    def create_new_garden(self):
        """Метод создания нового огорода в таблице бд"""
        self.cur.execute("INSERT INTO Garden(game_id) VALUES(?)", (self.game_id,))
        self.garden_id = self.cur.lastrowid
        self.window.garden_id = self.garden_id

        for i in range(6):
            self.cur.execute(
                "INSERT INTO Garden_field(garden_id, field, state, quantity_bites) VALUES(?, ?, ?, ?)",
                (self.garden_id, i, 0, 0),
            )
        self.con.commit()

    def get_garden_id(self):
        """Метод получения огорода для дальнейшей игры"""
        id = self.cur.execute(
            """SELECT id FROM Garden
                              WHERE game_id=?""",
            (self.game_id,),
        ).fetchone()
        self.garden_id = id[0]
        self.window.garden_id = self.garden_id
