import sqlite3

connection = sqlite3.connect("student.db")

cursor = connection.cursor()

table_info = """
Create table Student (Name VARCHAR(25), Class Varchar(25), Section Varchar(25));
"""

cursor.execute(table_info)

cursor.execute("""Insert into Student Values ('Sanchit', 'Data Science','A')""")
cursor.execute("""Insert into Student Values ('Singla', 'MLOPS','E')""")
cursor.execute("""Insert into Student Values ('Panku', 'Data Analyst','D')""")
cursor.execute("""Insert into Student Values ('Mannu', 'Data Engineer','C')""")
cursor.execute("""Insert into Student Values ('chunnu', 'Software engineer','B')""")
cursor.execute("""Insert into Student Values ('chunu', 'MLOPS','B')""")


print("The inserted records are")
data = cursor.execute('''Select * from Student''')
for row in data:
    print(row)


connection.commit()
connection.close()