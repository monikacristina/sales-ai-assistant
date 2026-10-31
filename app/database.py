import sqlite3

DATABASE_NAME = "data/sales.db"


def get_connection():
    """
    Establish a connection to the SQLite database.
    """
    connection = sqlite3.connect(DATABASE_NAME)

    # Allows us to access columns using their names.
    connection.row_factory = sqlite3.Row

    return connection


def create_table():
    """
    Create the sales table if it doesn't already exist.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            transaction_id TEXT PRIMARY KEY,
            transaction_date TEXT,
            product_name TEXT,
            category TEXT,
            quantity INTEGER,
            unit_price REAL,
            discount_amount REAL,
            region TEXT,
            sales_channel TEXT,
            status TEXT
        )
    """)

    connection.commit()
    connection.close()
