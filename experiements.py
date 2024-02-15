import sqlite3

def read_database(file_path):
    connection = sqlite3.connect(file_path)
    cursor = connection.cursor()
    cursor.execute("""SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = 'my_table'""")
    table_names = cursor.fetchall()
    print(table_names)


read_database("upload_database\data.db")