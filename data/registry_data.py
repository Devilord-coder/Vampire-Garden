import sqlite3
import hashlib


class RegistryDataBase:
    """ База данных для авторизации пользователей """

    def __init__(self):
        # Изначально соединение закрыто
        self.con = None
        self.cur = None
    
    def open(self):
        # открываем, если оно не открыто
        if not self.con:
            self.con = sqlite3.connect("vampire_garden_db.db")
            self.cur = self.con.cursor()
    
    def close(self):
        # закрываем, если открыто
        if self.con:
            self.con.close()
        self.con = None
        self.cur = None
    
    def update(self):
        # если соединени есть, обновляем
        if self.con:
            self.con.commit()

    def sha256_hash(self, password) -> str:
        """ Метод для хэширования пароля """

        sha256 = hashlib.sha256()
        sha256.update(password.encode("utf-8"))
        return sha256.hexdigest()

    def check_login(self, login) -> int:
        """ Метод проверки наличия логина в базе данных """

        # Если есть соединение проверить наличие
        if self.con:
            return self.cur.execute(
                "SELECT id FROM Registry WHERE login=?", (login,)
            ).fetchall()
        else: # иначе ошибка
            self.open()
            self.check_login(login)

    def add_user(self, name, email, login, password) -> str:
        """ Метод для добавления игроков в базу данных
        
        ==== RETURNS ====
            "OK" - если все прошло успешно
            "Пользователь с данным логином уже существует." - надо изменить логин
            "Все поля должны быть заполнены." - все значения не должны быть пустыми
        """
        
        if not self.con: # если нет открытой бд - ошибка
            self.open()
            self.add_user(name, email, login, password)
        if not all([name, email, login, password]):
            return "Все поля должны быть заполнены."
        if self.check_login(login):
            return "Пользователь с данным логином уже существует."

        hash_password = self.sha256_hash(password)
        self.cur.execute(
            "INSERT INTO Registry(name, login, password, email) VALUES (?, ?, ?, ?)",
            (name, login, hash_password, email),
        )
        self.update() # обновляем бд
        return "OK"

    def check_user(self, login, password) -> str:
        """ Метод для проверки правильности ввода данных для входа под существующим аккаунтом
        
        ==== RETURNS ====
            "OK" - если все прошло успешно
            "Пользователя с данным логином не существует." - неверный логин
            "Пароль введён неккоректно." - неверный пароль
        """

        if not self.con: # если нет открытой бд - ошибка
            self.open()
            self.check_user(login, password)
        if not self.check_login(login):
            return "Пользователя с данным логином не существует."

        hash_password = self.sha256_hash(password)
        correct_password = self.cur.execute(
            "SELECT password from Registry WHERE login=?", (login,)
        ).fetchall()
        if hash_password != correct_password[0][0]:
            return "Пароль введён неккоректно."
        return "OK"


registry_database = RegistryDataBase()
