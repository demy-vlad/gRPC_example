import sqlite3
from sqlite3 import Error

DATABASE_FILE = "users.db"

def create_connection():
    try:
        connection = sqlite3.connect(DATABASE_FILE)
        return connection
    except Error as e:
        print(e)
        return None

def create_tables(connection):
    create_users_table_query = '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        );
    '''
    try:
        cursor = connection.cursor()
        cursor.execute(create_users_table_query)
        connection.commit()
    except Error as e:
        print(e)

def register_user(email, password):
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
            connection.commit()
            connection.close()
            return True
        except Error as e:
            print(e)
    return False

def login_user(email, password):
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
            user = cursor.fetchone()
            connection.close()
            if user is not None:
                return True
        except Error as e:
            print(e)
    return False
