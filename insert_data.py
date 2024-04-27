import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('my_database.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Insert data into the 'users' table
cursor.execute('''
    INSERT INTO users (name, email) VALUES (?, ?)
''', ('John Doe', 'john@example.com'))

# Commit the transaction
conn.commit()

# Close the cursor
cursor.close()

# Close the connection
conn.close()
