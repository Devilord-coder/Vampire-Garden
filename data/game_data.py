class GameData:
    def __init__(self, window):
        self.window = window
        self.con = self.window.con
        self.cur = self.con.cursor()
        self.game_number = self.window.game_number
        self.login = None
        
    def get_user_id(self):
        self.login = self.window.login
        id = self.cur.execute('SELECT id FROM Registry WHERE login=?', (self.login,)).fetchone()
        return id[0]
        
    def get_game_state(self):
        self.login = self.window.login
        id = self.cur.execute('''SELECT Game.id FROM Game
                                  JOIN Registry on Game.user_id=Registry.id
                                  WHERE Game.game_number=? AND Registry.login=?''', (self.game_number, self.login)).fetchone()
        if id:
            return True
        
        user_id = self.get_user_id()
        self.cur.execute('INSERT INTO Game(user_id, game_number) VALUES(?, ?)', (user_id, self.game_number))
        self.con.commit()
        id = self.cur.lastrowid
        self.create_new_garden()
        return False
    
    def create_new_garden(self):
        pass