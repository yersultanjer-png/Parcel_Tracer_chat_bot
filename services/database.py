import sqlite3

DB_NAME = 'chatbot.db'


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS parcels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tracking_number TEXT UNIQUE NOT NULL,
            sender TEXT NOT NULL,
            receiver TEXT NOT NULL,
            city TEXT NOT NULL,
            status TEXT NOT NULL,
            parcel_type TEXT NOT NULL
        )
    ''')

    cursor.execute('SELECT COUNT(*) FROM parcels')
    count = cursor.fetchone()[0]

    if count == 0:
        demo_parcels = [
            ('KZT12345678', 'Aruzhan', 'Dias', 'Almaty', 'In transit', 'standard'),
            ('KZT87654321', 'Nursultan', 'Aigerim', 'Astana', 'Delivered', 'express'),
            ('KZT11223344', 'Ali', 'Madi', 'Shymkent', 'Created', 'standard'),
            ('KZT55667788', 'Dana', 'Asel', 'Karaganda', 'In transit', 'express')
        ]
        cursor.executemany(
            'INSERT INTO parcels (tracking_number, sender, receiver, city, status, parcel_type) VALUES (?, ?, ?, ?, ?, ?)',
            demo_parcels
        )

    conn.commit()
    conn.close()


def save_message(sender, message):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO messages (sender, message) VALUES (?, ?)', (sender, message))
    conn.commit()
    conn.close()


def get_history():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT sender, message FROM messages ORDER BY id ASC')
    rows = cursor.fetchall()
    conn.close()
    return rows


def clear_history():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM messages')
    conn.commit()
    conn.close()


def find_parcel_by_tracking(tracking_number):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT tracking_number, sender, receiver, city, status, parcel_type FROM parcels WHERE tracking_number = ?',
        (tracking_number,)
    )
    row = cursor.fetchone()
    conn.close()
    return row


def get_all_parcels():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT tracking_number, sender, receiver, city, status, parcel_type FROM parcels ORDER BY id ASC')
    rows = cursor.fetchall()
    conn.close()
    return rows
