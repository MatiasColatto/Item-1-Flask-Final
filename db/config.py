import sqlite3

def get_db_connection():
    conn = sqlite3.connect('db/tfinal.db')
    cur = conn.cursor()
    return cur, conn