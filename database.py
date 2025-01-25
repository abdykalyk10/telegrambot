import sqlite3
from datetime import date
from datetime import datetime

class Database:
    def __init__(self, path: str):
        self.path = path

    def create_table(self):
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                age INTEGER,
                phone_number TEXT,
                rate INTEGER,
                extra_comments TEXT,
                user_id INTEGER,
                date TEXT
            )''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS dishes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name_dish TEXT,
                price INTEGER,
                description TEXT,
                category TEXT
            )''')

    def save_complaint(self, data: dict):
        with sqlite3.connect(self.path) as conn:
            conn.execute('''
            INSERT INTO reviews(name, age, phone_number, rate, extra_comments, user_id, date) 
            VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (data['name'], data['age'], data['phone_number'],
             data['rate'], data['extra_comments'], data['user_id'],
             data.get('date', datetime.now().strftime('%d/%m/%y'))))

    def save_dish(self, dish_data: dict):

            with sqlite3.connect(self.path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                        INSERT INTO dishes (name_dish, description, price, category) 
                        VALUES (?, ?, ?, ?)""",
                                   (dish_data['name_dish'], dish_data['description'], dish_data['price'],
                                    dish_data['category']))


    def get_dishes(self):
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            result = cursor.execute('SELECT * FROM dishes')
            result.row_factory = sqlite3.Row
            data = result.fetchall()
            return [dict(row) for row in data]


    def get_reviews(self):

            with sqlite3.connect(self.path) as conn:
                cursor = conn.cursor()
                result = cursor.execute('SELECT * FROM reviews')
                result.row_factory = sqlite3.Row
                data = result.fetchall()

            return [dict(row) for row in data]