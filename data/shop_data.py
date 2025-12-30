class ShopData:
    """Класс для работы с бд в магазине"""

    def __init__(self, window):
        self.window = window
        self.con = self.window.con
        self.cur = self.con.cursor()
        self.game_id = self.window.game_id
        self.quantity_money = window.quantity_money
        self.setup()

    def setup(self):
        """Получение данных игры"""
        quantity_seeds = self.cur.execute(
            """SELECT quantity_mandragora_seeds, quantity_belladonna_seeds, quantity_rose_seeds
                                           FROM Game WHERE id=?""",
            (self.game_id,),
        ).fetchone()
        self.quantity_mandragora_seeds = quantity_seeds[0]
        self.quantity_belladonna_seeds = quantity_seeds[1]
        self.quantity_rose_seeds = quantity_seeds[2]

    def save(self):
        """Сохранение всех данных с магазина во всей игре"""
        self.cur.execute(
            """UPDATE Game
                         SET quantity_money=?, quantity_mandragora_seeds=?, quantity_belladonna_seeds=?, quantity_rose_seeds=?
                         WHERE id=?""",
            (
                self.quantity_money,
                self.quantity_mandragora_seeds,
                self.quantity_belladonna_seeds,
                self.quantity_rose_seeds,
                self.game_id,
            ),
        )
        self.con.commit()
