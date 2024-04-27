import mysql.connector

# AWS RDS database configuration
config = {
    'user': 'wallet',
    'password': 'xP5cP5rZ1gU5jE9p',
    'host': 'database-1.c72eiu8keywt.us-east-1.rds.amazonaws.com',
    'database': 'wallet'
}

try:
    # Connect to the database
    connection = mysql.connector.connect(**config)

    if connection.is_connected():
        print('Connected to the MySQL database')

        # Create a cursor object to execute queries
        cursor = connection.cursor()

        # Example query: Select all records from a table
        query = 'select * from cards;'
        cursor.execute(query)

        # Fetch and print the results
        rows = cursor.fetchall()
        for row in rows:
            print(row)

except mysql.connector.Error as e:
    print('Error:', e)

finally:
    # Close the cursor and connection
    if 'cursor' in locals():
        cursor.close()
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print('Connection closed')
