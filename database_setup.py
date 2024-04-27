import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('my_database.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()
# cursor.execute('DROP table cards')
# Create tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS stores (
        card_name TEXT,
        store_name TEXT
    )
''')

# Create a new table for cards with name and amount of money
cursor.execute('''
    CREATE TABLE IF NOT EXISTS cards (
        card_name TEXT,
        expiration TEXT,
        amount INTEGER
    )
''')

cursor.execute('DELETE FROM cards')

cursor.execute('DELETE FROM stores')

# Insert data into the 'card_money' table
cards_data = [
    ('rav tav','04/26', 100),
    ('buyme','08/29', 200),
    ('nufshonit','01/32', 150)
]
cursor.executemany('INSERT INTO cards (card_name,expiration,amount) VALUES (?,?,?)', cards_data)

# Insert data into the 'stores' table
stores_data = [
    ('rav tav', 'fox'),
    ('buyme', 'h&m'),
    ('nufshonit', 'castro'),
    ('rav tav', 'castro')

]
cursor.executemany('INSERT INTO stores (card_name, store_name) VALUES (?, ?)', stores_data)

# Commit changes and close the cursor and connection
conn.commit()
cursor.close()
conn.close()
