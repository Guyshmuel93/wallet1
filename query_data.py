import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('my_database.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Retrieve a list of all tables in the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

# Print the list of tables
# for table in tables:
#     print(table[0])
# print(conn.filename)
#
# Query data from the 'users' table
cursor.execute('''
    SELECT * FROM cards

''')

# Fetch all rows from the result set
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close the cursor
cursor.close()

# Close the connection
conn.close()
