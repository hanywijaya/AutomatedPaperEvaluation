from Database import Database
from random import randint
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
class Users:
    def __init__(self):
        self.conn = Database().conn
        self.data = None

    def getAll(self):
        self.data = []
        data = self.conn.execute("SELECT * FROM user").fetchall()
        self.conn.close()
        return data

    def getOne(self,id):
        self.data = []
        data = self.conn.execute("SELECT * FROM user where id = "+str(id)).fetchone()
        self.conn.close()
        return data
    
    def authenticate(self, username, password):
        self.data = [] 
        user = self.conn.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()
        self.conn.close()
        
        if check_password_hash(user['pass'], password) == False:
            # error message for wrong password
            user = None

        return user

    def getCode(self, randomcode):
        self.data = []
        user = self.conn.execute('SELECT * FROM user WHERE randomcode = ?', (randomcode,)).fetchone()
        self.conn.close()

        return user
    
    def getEmail(self, email):
        self.data = []
        user = self.conn.execute('SELECT * FROM user WHERE email = ?', (email,)).fetchone()
        self.conn.close()

        return user

    def insert(self, username, email, password, randomcode):
        conn = get_db_connection()
        # cursor = conn.cursor()
        password_hashed = generate_password_hash(password)
        conn.execute('INSERT INTO user (username, email, pass, randomcode, DefiniteUser) VALUES (?, ?, ?, ?, ?)',
                       (username, email, password_hashed, randomcode, 0))
        
        conn.commit()
        conn.close()
    
    def setDefinite(self, token):
        conn = get_db_connection()
        
        conn.execute('UPDATE user SET DefiniteUser = 1 WHERE randomcode = ?',
                       (token,))
        
        conn.commit()
        conn.close()
    
    def updatePassword(self, token, password):
        conn = get_db_connection()
        password_hashed = generate_password_hash(password)
        conn.execute('UPDATE user SET pass = ? WHERE randomcode = ?',
                        (password_hashed, token))
        conn.commit()
        conn.close()
