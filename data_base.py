import sqlite3


conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()


# cursor.execute('''
# CREATE TABLE IF NOT EXISTS my_table (
#     id INTEGER PRIMARY KEY,
#     link TEXT NOT NULL UNIQUE,
# )
# ''')

# api_id = '28312933'
# api_hash = '1f75793fc211a5eb3812a860cfe6c713'
# phone_number = '+998883601656'


def add_data(link):
    try:
        cursor.execute('INSERT INTO my_table (link) VALUES (?)', (link))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"{link} allaqachon mavjud, qo'shilmadi.")

conn.close()
