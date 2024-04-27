import mysql
from mysql import db_config, DatabaseManager

def main():
    # Import database configuration from MySQL.py
    from mysql import db_config

    # Initialize DatabaseManager with configuration
    db_manager = DatabaseManager(db_config)

    # Connect to the database
    db_manager.connect()

    # Example data to insert
    data_to_insert = {
        'card_name': 'rav tav',
        'expiration': '05/58',
        'amount': '120'
    }
    rows= db_manager.execute_query("CREATE TABLE IF NOT EXISTS cards (card_name VARCHAR(255) PRIMARY KEY,expiration "
                                   "VARCHAR(255) NOT NULL, amount INT NOT NULL)")
    print(rows)
    mysql.DatabaseManager.insert_data(db_manager,"cards",data_to_insert)
    rows= db_manager.execute_query("select * from cards;")
    print(rows)

    # Example table to insert data into
    table_name = 'your_table'

    # Insert data into the table
    # db_manager.insert_data(table_name, data_to_insert)

    # Disconnect from the database
    db_manager.disconnect()

if __name__ == "__main__":
    main()