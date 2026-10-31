from app.database import create_table, get_connection

# Create the table
create_table()

print("Database and table created successfully!")

# Verify table creation
connection = get_connection()

cursor = connection.cursor()

cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type='table'
""")

tables = cursor.fetchall()

print("Tables in database:")

for table in tables:
    print(table["name"])

connection.close()
