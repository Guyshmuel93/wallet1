import mysql.connector

# Define the connection parameters
config = {
    'user': 'wallet',
    'password': 'xP5cP5rZ1gU5jE9p',
    'host': 'database-1.c72eiu8keywt.us-east-1.rds.amazonaws.com',
    'database': 'wallet'
}

# Establish the connection
try:
    connection = mysql.connector.connect(**config)
    print("Connected to MySQL database")

    # Create a cursor object
    cursor = connection.cursor()

    # Define the CREATE TABLE statement
    create_table_query = """
    CREATE TABLE IF NOT EXISTS cards (
        card_name VARCHAR(255) PRIMARY KEY,
        expiration VARCHAR(255) NOT NULL,
        amount INT NOT NULL
    )
    """

    # Execute the CREATE TABLE statement
    cursor.execute(create_table_query)
    print("Table 'users' created successfully")

    # Define the INSERT INTO statement
    insert_data_query = """
    INSERT INTO cards (card_name, expiration, amount) VALUES
    ('rav tav', '04/26', 100),
    ('buyme', '08/29', 200),
    ('nufshonit', '01/32', 150)
    """


# Execute the INSERT INTO statement
    cursor.execute(insert_data_query)
    print("Data inserted successfully")

    # Commit changes to the database
    connection.commit()

except mysql.connector.Error as error:
    print("Error:", error)

finally:
    # Close cursor and connection
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print("Connection closed")
