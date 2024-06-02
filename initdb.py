import sqlite3
from Models.Users import Users

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# user = Users()
# user.insert('test', 'testing@gmail.com', '12345678', 372293)


connection.commit()
connection.close()