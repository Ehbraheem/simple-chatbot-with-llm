import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL') or 'database.db'

connection = sqlite3.connect(DATABASE_URL)

with open('schema.sql') as f:
    connection.executescript(f.read())

cursor = connection.cursor()

print(cursor.execute('SELECT count(*) from users').fetchall())
print(cursor.execute('SELECT count(*) from chats').fetchall())

connection.close()

