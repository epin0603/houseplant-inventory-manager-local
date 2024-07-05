import sqlite3

def get_db_connection():
    conn = sqlite3.connect('houseplants.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS plants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            common_name TEXT NOT NULL,
            scientific_name TEXT,
            purchase_date TEXT,
            care_history TEXT,
            image_path TEXT
        )
    ''')
    conn.commit()
    conn.close()
