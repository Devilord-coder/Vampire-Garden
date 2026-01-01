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
            """SELECT quantity_money quantity_mandragora_seeds, quantity_belladonna_seeds, quantity_rose_seeds, quantity_mandragora, quantity_belladonna, quantity_rose, quantity_bats, quantity_sceletons, quantity_werewolves FROM Game
                                                 JOIN Registry on Game.user_id=Registry.id
                                                 WHERE login=?""",
            (self.login,),
        ).fetchone()
