import psycopg2
import pandas as pd

def get_connection():
    return psycopg2.connect(
        dbname="supp_inv_db",
        user="regan_supp_inv_db",
        password="regan_supp_inv_db",
        host="localhost",
        port="5432"
    )

def execute_query(query, params=()):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            if cursor.description:  # Check if the query returns data
                return pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
            return None  # For queries that don't return data
        
def close_connection(conn):
    conn.close()