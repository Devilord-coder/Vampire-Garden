class GardenData:
    """Класс для работы с бд огорода для синхронизации игры"""

    def __init__(self, window):
        self.window = window
        self.con = self.window.con
        self.cur = self.con.cursor()
        self.game_id = self.window.game_id
        self.garden_id = self.window.garden_id
        self.login = self.window.login
        self.fields = []
        self.setup()

    def setup(self):
        """Метод переноса данных огорода из бд в переменные"""
        for i in range(6):
            field_information = self.cur.execute(
                """SELECT plant_name, state, quantity_bites FROM Garden_field
                                                 LEFT JOIN Plants on Plants.id=Garden_field.plant_id
                                                 WHERE garden_id=? AND field=?""",
                (self.garden_id, i),
            ).fetchone()
            self.fields.append(
                {
                    "plant_name": field_information[0],
                    "state": field_information[1],
                    "quantity_bites": field_information[2],
                }
            )

        quantity_plants = self.cur.execute(
            """SELECT quantity_mandragora_seeds, quantity_belladonna_seeds, quantity_rose_seeds,
            quantity_planted_mandragora, quantity_planted_belladonna, quantity_planted_rose FROM Game
                                           WHERE id=?""",
            (self.game_id,),
        ).fetchone()
        self.quantity_mandragora_seeds = quantity_plants[0]
        self.quantity_belladonna_seeds = quantity_plants[1]
        self.quantity_rose_seeds = quantity_plants[2]
        self.quantity_planted_mandragora = quantity_plants[3]
        self.quantity_planted_belladonna = quantity_plants[4]
        self.quantity_planted_rose = quantity_plants[5]

        quantity_plants = self.cur.execute(
            """SELECT quantity_mandragora, quantity_belladonna, quantity_rose
                                           FROM Game WHERE id=?""",
            (self.game_id,),
        ).fetchone()
        self.quantity_mandragora = quantity_plants[0]
        self.quantity_belladonna = quantity_plants[1]
        self.quantity_rose = quantity_plants[2]

    def save(self):
        """Метод сохранения состояния игры в бд"""
        for i in range(6):
            plant_name = self.fields[i]["plant_name"]
            state = self.fields[i]["state"]
            quantity_bites = self.fields[i]["quantity_bites"]
            if plant_name:
                plant_id = self.get_plant_id(plant_name)
            else:
                plant_id = None

            self.cur.execute(
                """UPDATE Garden_field
                             SET plant_id=?, state=?, quantity_bites=?
                             WHERE garden_id=? AND field=?""",
                (plant_id, state, quantity_bites, self.garden_id, i),
            )

        self.cur.execute(
            """UPDATE Game
                         SET quantity_mandragora_seeds=?, quantity_belladonna_seeds=?, quantity_rose_seeds=?,
                         quantity_mandragora=?, quantity_belladonna=?, quantity_rose=?,
                         quantity_planted_mandragora=?, quantity_planted_belladonna=?, quantity_planted_rose=?
                         WHERE id=?""",
            (
                self.quantity_mandragora_seeds,
                self.quantity_belladonna_seeds,
                self.quantity_rose_seeds,
                self.quantity_mandragora,
                self.quantity_belladonna,
                self.quantity_rose,
                self.quantity_planted_mandragora,
                self.quantity_planted_belladonna,
                self.quantity_planted_rose,
                self.game_id,
            ),
        )
        self.con.commit()

    def get_plant_id(self, name):
        """Получение id растения по названию"""
        id = self.cur.execute(
            "SELECT id FROM Plants WHERE plant_name=?", (name,)
        ).fetchone()
        return id[0]

    def update_quantity_bites(self, quantity_bites, field_number):
        """Обновление количества укусов в бд"""
        self.cur.execute(
            """UPDATE Garden_field
                         SET quantity_bites=?
                         WHERE field=? and garden_id=?""",
            (quantity_bites, field_number, self.garden_id),
        )
        self.con.commit()

    def get_user_id(self):
        """Метод получения id пользователя по логину"""
        return self.cur.execute(
            "SELECT id FROM Registry WHERE login=?", (self.login,)
        ).fetchone()[0]

    def check_final(self):
        """Метод проверки конца игры"""
        user_id = self.get_user_id()
        plants = self.cur.execute(
            """SELECT quantity_mandragora, quantity_belladonna, quantity_rose FROM Game
                                  WHERE user_id=? and id=?""",
            (user_id, self.game_id),
        ).fetchone()
        if plants[0] >= 50 and plants[1] >= 30 and plants[2] >= 25:
            return True
        return False

    def update(self):
        """Метод обновления бд для синхронизации со всей игрой"""
        self.setup()
