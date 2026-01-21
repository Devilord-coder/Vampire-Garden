class StatisticData:
    def __init__(self, window):
        self.window = window
        self.con = self.window.con
        self.cur = self.con.cursor()
        self.game_number = self.window.game_number
        self.login = self.window.login
        self.game_id = self.window.game_id
        self.setup()

    def setup(self):
        """Получение имени пользавателя и всех данных статистики"""
        self.name = self.cur.execute(
            """SELECT name FROM Registry
                                     WHERE login=?""",
            (self.login,),
        ).fetchone()[0]
        self.game_information = self.cur.execute(
            """SELECT quantity_money, quantity_mandragora_seeds, quantity_belladonna_seeds, quantity_rose_seeds,
            quantity_mandragora, quantity_belladonna, quantity_rose, quantity_bats, quantity_sceletons,
            quantity_werewolves FROM Game
                                                 JOIN Registry on Game.user_id=Registry.id
                                                 WHERE login=?""",
            (self.login,),
        ).fetchone()

    def get_user_id(self):
        """Метод получения id пользователя по логину"""
        return self.cur.execute(
            "SELECT id FROM Registry WHERE login=?", (self.login,)
        ).fetchone()[0]

    def matching_name_column(self, name):
        """Соотношение названия бойца с колонкой в бд"""
        if name == "bat":
            return "quantity_bats"
        elif name == "sceleton":
            return "quantity_sceleton"
        elif name == "werewolf":
            return "quantity_werewolves"

    def get_quantity_minions(self, column):
        """Получение количество бойцов по названию на данный момент из бд"""
        quantity = self.cur.execute(
            f"""SELECT {column} FROM Game
                                         JOIN Registry on Game.user_id=Registry.id
                                         WHERE login=?""",
            (self.login,),
        ).fetchone()
        return quantity[0]

    def update_minions_information(self, name, quantity_money):
        """Обновление количества бойцов при покупке в бд"""
        column = self.matching_name_column(name)
        quantity = self.get_quantity_minions(column)
        quantity += 1
        self.cur.execute(
            f"""UPDATE Game
                         SET {column}=?, quantity_money=?
                         WHERE user_id=?""",
            (quantity, quantity_money, self.get_user_id()),
        )
        self.con.commit()

    def get_quntity_money(self):
        """Получение количства денег"""
        quantity = self.cur.execute(
            """SELECT quantity_money FROM Game
                                         JOIN Registry on Game.user_id=Registry.id
                                         WHERE login=?""",
            (self.login,),
        ).fetchone()
        quantity = quantity[0]
        if not quantity:
            quantity = 0
        return quantity

    def update(self):
        """Метод обновления бд для синхронизации со всей игрой"""
        self.setup()
