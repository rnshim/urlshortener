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

def list_urls(sqlite_file):
    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM urls")
    rows = cursor.fetchall()
    conn.close()
    column_names = [description[0] for description in cursor.description]
    result = [dict(zip(column_names, row)) for row in rows]
    return result

def retrieve(sqlite_file, alias):
    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()
    cursor.execute("SELECT url FROM urls WHERE alias=?", (alias,))
    row = cursor.fetchone()
    conn.close()
    print("alias " + alias)
    print(row[0])
    return row[0] if row is not None else None

def get_number_of_entries(sqlite_file):
    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM urls")
    row = cursor.fetchone()
    conn.close()
    return row[0] if row is not None else None