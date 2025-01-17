import sqlite3

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
                extra_comments TEXT
            )''')

    def save_complaint(self, data: dict):
        with sqlite3.connect(self.path) as conn:
            conn.execute('''
            INSERT INTO reviews(name, age, phone_number, rate, extra_comments, user_id) 
            VALUES (?, ?, ?, ?, ?, ?)''',
            (data['name'], data['age'], data['phone_number'], data['rate'], data['extra_comments'], data['user_id']))

    def user_id(self):
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            ALTER TABLE reviews
            ADD COLUMN User_ID INTEGER
            ''')