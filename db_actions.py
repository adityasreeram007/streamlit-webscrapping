import sqlite3
import os
import pandas as pd
# Database file path
db_path = 'bus_routes.db'
def load_data():
    conn = sqlite3.connect('bus_routes.db')
    query = "SELECT * FROM bus_routes"
    df = pd.read_sql_query(query, conn)
    return df
def createDB():
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_path)

    # Create a cursor object
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS bus_routes')
    # Create the bus_routes table if it doesn't exist
    c.execute('''
        CREATE TABLE  bus_routes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            route_name TEXT,
            route_link TEXT,
            busname TEXT,
            bustype TEXT,
            departing_time DATETIME,
            duration TEXT,
            reaching_time DATETIME,
            star_rating TEXT,
            price TEXT,
            seats_available TEXT
        )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()



def insert_data( data):
    # Create a cursor object
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # SQL query to insert data into the bus_routes table
    query = '''
        INSERT INTO bus_routes (
            route_name, route_link, busname, bustype, 
            departing_time, duration, reaching_time, 
            star_rating, price, seats_available
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''

    # Execute the query for each row of data
    for row in data:
        c.execute(query, row)

    # Commit the changes
    conn.commit()
    conn.close()


def get_first_n_rows( n=10):
    # Create a cursor object
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # SQL query to get the first n rows from the bus_routes table
    query = 'SELECT * FROM bus_routes LIMIT ?'

    # Execute the query
    c.execute(query, (n,))

    # Fetch the results
    rows = c.fetchall()

    # Return the results
    return rows
