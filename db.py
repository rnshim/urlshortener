import sqlite3


def create(sqlite_file):
    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS urls (
                   id INTEGER PRIMARY KEY,
                   url TEXT NOT NULL,
                   alias TEXT NOT NULL UNIQUE,
                   timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()

def insert(sqlite_file, url, alias):
    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO urls (url, alias) VALUES (?, ?)", (url, alias))
    conn.commit()
    conn.close()

def delete_url(sqlite_file, alias):
    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM urls WHERE alias=?", (alias,))
    conn.commit()
    conn.close()

def list_(sqlite_file):
    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()
    cursor.execute("SELECT url FROM urls")
    rows = cursor.fetchall()
    conn.close()
    return rows

def retrieve(sqlite_file, alias):
    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()
    cursor.execute("SELECT url FROM urls WHERE alias=?", (alias,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None
