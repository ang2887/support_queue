# neon_post_data.py

import os
import psycopg2
from dotenv import load_dotenv
from data_generator import *

load_dotenv()

USE_NEON = os.getenv("USE_NEON", "0") == "1"
DATABASE_URL = os.getenv("NEON_DB_URL") if USE_NEON else os.getenv("SUPABASE_DB_URL")

# Create a connection to PostgreSQL using psycopg2
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# Define the params to pass to the data generator
params = {
    'NUM_COMPANIES':  50,
    'NUM_USERS': 1000,
    'NUM_SUPPORT_STAFF': 50,
    'NUM_TICKETS': 5000, 
    'TICKET_CATEGORIES': ['Technical', 'Billing', 'Account', 'General Inquiry'],
    'mean': 2,
    'sigma': 1,
    'user_probs_limit': 100
}

# Generate the data using the support_queue_data_generator function with the params
tables = support_queue_data_generator(params)

# Define a function to insert data row by row into PostgreSQL
def insert_data(table_name, df, cursor, conn):
    # Get columns from the dataframe
    columns = ', '.join(df.columns)
    
    # Create the values placeholder (e.g., %s, %s, %s)
    values_placeholder = ', '.join(['%s' for _ in df.columns])
    
    # SQL Insert query
    insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({values_placeholder})"
    
    # Insert data row by row
    for row in df.itertuples(index=False, name=None):
        cursor.execute(insert_query, row)
    
    # Commit the transaction after inserting all rows
    conn.commit()

# Insert data into each table manually
for table_name, df in tables.items():
    try:
        insert_data(table_name, df, cur, conn)
        print(f"Inserted data into {table_name}")
    except Exception as e:
        print(f"Error inserting into {table_name}: {e}")

# Close the connection
cur.close()
conn.close()