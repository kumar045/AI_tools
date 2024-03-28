import sqlite3 

sqliteConnection = sqlite3.connect('db.sqlite3')
cursor = sqliteConnection.cursor()
print("Connected to SQLite")

# Deleting single record now
sql_delete_query = """DELETE from apiAppCellebrite_zipfilemodel where id = 2"""
cursor.execute(sql_delete_query)
sqliteConnection.commit()
print("Record deleted successfully ")
cursor.close()