import sqlite3
DATABASE = "url_shortener.db"

def create():
    conn = sqlite3.connect(DATABASE)
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

def insert(url, alias):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO urls (url, alias) VALUES (?, ?)", (url, alias))
    conn.commit()
    conn.close()

def delete_url(alias):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM urls WHERE alias=?", (alias,))
    conn.commit()
    conn.close()

def list():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT url FROM urls")
    rows = cursor.fetchall()
    conn.close()
    return rows

def retrieve(alias):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT url FROM urls WHERE alias=?", (alias,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None
