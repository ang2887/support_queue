# neon_test_connection.py

import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

USE_NEON = os.getenv("USE_NEON", "0") == "1"
DATABASE_URL = os.getenv("NEON_DB_URL") if USE_NEON else os.getenv("SUPABASE_DB_URL")

def test_db_connection():
    try:
        print(f"🔄 Connecting to {'Neon' if USE_NEON else 'Supabase'} database...")
        conn = psycopg2.connect(DATABASE_URL)
        
        # Write a simple SQL query
        query_companies = "SELECT * FROM companies LIMIT 5"

        # Execute the query using the psycopg2 connection object
        df = pd.read_sql(query_companies, con=conn)
        print(df.head())

        conn.close()
    except Exception as e:
        print(f"Error connecting to the database: {e}")

if __name__ == '__main__':
    test_db_connection()