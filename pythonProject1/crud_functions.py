import sqlite3

connection = sqlite3.connect('crud_functions.db')
cursor = connection.cursor()


for num in range(2, 5):
    cursor.execute("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)",
               (f"product{num}", f"description{num}", 100 * num))

connection.commit()


def initiate_db():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users(
            user_id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER NOT NULL,
            balance INTEGER NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products(
            user_id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            price INTEGER NOT NULL
        )
        ''')
    connection.commit()


def get_all_products():
    cursor.execute("SELECT * FROM Products")
    result = cursor.fetchall()
    return result


def add_user(username, email, age):
    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, 1000)",
                   (username, email, age))
    connection.commit()


def is_included(username):
    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()
    for user in users:
        if user[1] == username:
            return True
    return False