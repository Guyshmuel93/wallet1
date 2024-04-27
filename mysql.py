import pymysql

# Define database configuration
db_config = {
    'user': 'wallet',
    'password': 'xP5cP5rZ1gU5jE9p',
    'host': 'database-1.c72eiu8keywt.us-east-1.rds.amazonaws.com',
    'database': 'wallet',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

class DatabaseManager:
    def __init__(self, config):
        self.connection = None
        self.config = config

    def connect(self):
        try:
            self.connection = pymysql.connect(**self.config)
            print("Connected to MySQL database")
        except pymysql.Error as error:
            print("Error:", error)

    def disconnect(self):
        if self.connection and self.connection.open:
            self.connection.close()
            print("Connection closed")

    def execute_query(self, query):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                self.connection.commit()
                return rows
        except pymysql.Error as error:
            print("Error executing query:", error)
            return []

    def insert_data(self, table, data):
        if not self.connection or not self.connection.open:
            print("Connection is not established.")
            return

        try:
            with self.connection.cursor() as cursor:
                placeholders = ', '.join(['%s'] * len(data))
                columns = ', '.join(data.keys())
                sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
                cursor.execute(sql, list(data.values()))
                self.connection.commit()
                print("Data inserted successfully")
        except pymysql.Error as error:
            print("Error inserting data:", error)



if __name__ == "__main__":
    # db_config = {
    #     'user': 'wallet',
    #     'password': 'xP5cP5rZ1gU5jE9p',
    #     'host': 'database-1.c72eiu8keywt.us-east-1.rds.amazonaws.com',
    #     'database': 'wallet',
    #     'charset': 'utf8mb4',
    #     'cursorclass': pymysql.cursors.DictCursor
    # }

    # Initialize DatabaseManager with configuration
    db_manager = DatabaseManager(db_config)

    # Connect to the database
    db_manager.connect()

    # Example query
    query = "SELECT * FROM your_table"
    result = db_manager.execute_query(query)
    print("Query Result:")
    for row in result:
        print(row)

    # Example data to insert
    data_to_insert = {
        'column1': 'value1',
        'column2': 'value2',
        'column3': 'value3'
    }

    # Example table to insert data into
    table_name = 'your_table'

    # Insert data into the table
    db_manager.insert_data(table_name, data_to_insert)

    # Disconnect from the database
    db_manager.disconnect()
