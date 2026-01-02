class GardenData:
    """Класс для работы с бд огорода для синхронизации игры"""

    def __init__(self, window):
        self.window = window
        self.con = self.window.con
        self.cur = self.con.cursor()
        self.game_id = self.window.game_id
        self.garden_id = self.window.garden_id
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

        quantity_seeds = self.cur.execute(
            """SELECT quantity_mandragora_seeds, quantity_belladonna_seeds, quantity_rose_seeds FROM Game
                                           WHERE id=?""",
            (self.game_id,),
        ).fetchone()
        self.quantity_mandragora_seeds = quantity_seeds[0]
        self.quantity_belladonna_seeds = quantity_seeds[1]
        self.quantity_rose_seeds = quantity_seeds[2]

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
                         SET quantity_mandragora_seeds=?, quantity_belladonna_seeds=?, quantity_rose_seeds=?
                         WHERE id=?""",
            (
                self.quantity_mandragora_seeds,
                self.quantity_belladonna_seeds,
                self.quantity_rose_seeds,
                self.game_id,
            ),
        )

        self.cur.execute(
            """UPDATE Game
                         SET quantity_mandragora=?, quantity_belladonna=?, quantity_rose=?
                         WHERE id=?""",
            (
                self.quantity_mandragora,
                self.quantity_belladonna,
                self.quantity_rose,
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

    def update(self):
        """Метод обновления бд для синхронизации со всей игрой"""
        self.setup()
