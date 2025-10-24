import sqlite3

def init_db():
    conn = sqlite3.connect("files.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_name TEXT,
                    file_id TEXT,
                    caption TEXT,
                    upload_date TEXT
                )''')
    conn.commit()
    conn.close()

def add_file(file_name, file_id, caption, upload_date):
    conn = sqlite3.connect("files.db")
    c = conn.cursor()
    c.execute("INSERT INTO files (file_name, file_id, caption, upload_date) VALUES (?, ?, ?, ?)",
              (file_name, file_id, caption, upload_date))
    conn.commit()
    conn.close()

def search_file(keyword):
    conn = sqlite3.connect("files.db")
    c = conn.cursor()
    c.execute("SELECT file_name, file_id FROM files WHERE file_name LIKE ? OR caption LIKE ?", 
              (f'%{keyword}%', f'%{keyword}%'))
    results = c.fetchall()
    conn.close()
    return results

def delete_file(filename):
    conn = sqlite3.connect("files.db")
    c = conn.cursor()
    c.execute("DELETE FROM files WHERE file_name=?", (filename,))
    conn.commit()
    conn.close()
