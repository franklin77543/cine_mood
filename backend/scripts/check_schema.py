import sqlite3

conn = sqlite3.connect('cinemood.db')
cursor = conn.cursor()
cursor.execute('PRAGMA table_info(genres)')

print('Genres table structure:')
for row in cursor.fetchall():
    print(row)

conn.close()
