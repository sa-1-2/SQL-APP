import sqlite3

def read_database(file_path):
    connection = sqlite3.connect(file_path)
    cursor = connection.cursor()
    cursor.execute("""SELECT name FROM sqlite_master WHERE type='table';""")
    table_names = cursor.fetchall()
    if table_names:
        table = table_names[0][0]
        cursor.execute(f"PRAGMA table_info({table})")
        rows = cursor.fetchall()
        column_names = [row[1] for row in rows]
    else:
        column_names=[]
    connection.close()
    return table, column_names


