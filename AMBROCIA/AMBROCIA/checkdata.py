import mysql.connector

# Replace the placeholders with your actual MySQL connection details
host = "localhost"
user = "root"
password = "pranjal@214022"
database = "ambrocia"

db = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

# Create a cursor object to execute queries
cursor = db.cursor()

# Fetch table metadata
cursor.execute("SHOW TABLES")

# Process the table metadata
tables = cursor.fetchall()
for table in tables:
    table_name = table[0]
    print(f"Table: {table_name}")

    # Fetch column names
    cursor.execute(f"SHOW COLUMNS FROM {table_name}")
    columns = cursor.fetchall()
    column_names = [column[0] for column in columns]

    # Fetch data from the table
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    for row in rows:
        row_data = dict(zip(column_names, row))
        print(row_data)

    print()  # Add a blank line between tables

# Close the cursor and database connection
cursor.close()
db.close()
