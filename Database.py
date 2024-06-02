import sqlite3
class Database:
    def __init__(self, sqliteFile = "database.db"):
        self.conn = sqlite3.connect('database.db')
        self.conn.row_factory = sqlite3.Row
        self.data = None


import sqlite3
conn = sqlite3.connect('example.db')
print("Connection established ..........")
