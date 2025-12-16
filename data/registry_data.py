import sqlite3
import hashlib
from .database_error import DataBaseError


class RegistryDataBase:
    """ База данных для авторизации пользователей """

    def __init__(self):
        self.con = None
        self.cur = None
    
    def open(self):
        if not self.con:
            self.con = sqlite3.connect("vampire_garden_db.db")
            self.cur = self.con.cursor()
    
    def close(self):
        if self.con:
            self.con.close()
        self.con = None
        self.cur = None
    
    def update(self):
        if self.con:
            self.con.commit()

    def sha256_hash(self, password):
        """ Метод для хэширования пароля """

        sha256 = hashlib.sha256()
        sha256.update(password.encode("utf-8"))
        return sha256.hexdigest()

    def check_login(self, login):
        """ Метод проверки наличия логина в базе данных """

        if self.con:
            return self.cur.execute(
                "SELECT id FROM Registry WHERE login=?", (login,)
            ).fetchall()
        else:
            raise DataBaseError("There is no opened database")

    def add_user(self, name, email, login, password):
        """ Метод для добавления игроков в базу данных """
        
        if not self.con:
            raise DataBaseError("There is no opened database")
        if not all([name, email, login, password]):
            return "Все поля должны быть заполнены."
        if self.check_login(login):
            return "Пользователь с данным логином уже существует."

        hash_password = self.sha256_hash(password)
        self.cur.execute(
            "INSERT INTO Registry(name, login, password, email) VALUES (?, ?, ?, ?)",
            (name, login, hash_password, email),
        )
        self.update()
        return "OK"

    def check_user(self, login, password):
        """ Метод для проверки правильности ввода данных для входа под существующим аккаунтом """

        if not self.con:
            raise DataBaseError("There is no opened database")
        if not self.check_login(login):
            return "Пользователя с данным логином не существует."

        hash_password = self.sha256_hash(password)
        correct_password = self.cur.execute(
            "SELECT password from Registry WHERE login=?", (login,)
        ).fetchall()
        if hash_password != correct_password[0][0]:
            return "Пароль введён неккоректно."
        return "OK"


database = RegistryDataBase()