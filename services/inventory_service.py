import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import database as db
import pandas as pd

from psycopg2.extras import execute_values

def update_inventory(current_date: pd.Timestamp):

    query = """
    SELECT
        DISTINCT ON (supplement_id) i.*,
        d.dosage_per_day
    FROM
        fact.inventory i
    JOIN 
        dim.dosage_data d ON i.supplement_id = d.supplement_id
    ORDER BY
        supplement_id,
        last_updated DESC;
    """

    latest_inventory = db.execute_query(query)

    # Calculate daily dosage for each supplement
    latest_inventory['days_since_update'] = (current_date - latest_inventory['last_updated']).dt.days
    latest_inventory['qty_use_since_update'] = latest_inventory['days_since_update'] * latest_inventory['dosage_per_day']
    latest_inventory['qty_remaining'] = latest_inventory['qty_remaining'] - latest_inventory['qty_use_since_update']
    latest_inventory = latest_inventory[['user_id', 'supplement_id', 'qty_remaining', 'last_updated']]
    latest_inventory['last_updated'] = current_date
    

    # Convert DataFrame to a list of tuples (one tuple per row)
    # Convert DataFrame rows to a list of tuples
    params = [tuple(row) for row in latest_inventory.to_numpy()]
    
    insert_query = "INSERT INTO fact.inventory (user_id, supplement_id, qty_remaining, last_updated) VALUES %s"
    
    # conn = db.get_connection()  # Assuming your db module exposes a connection method
    # with conn.cursor() as cursor:
    #     execute_values(cursor, insert_query, params)
    # conn.commit()
    print(latest_inventory)
    return latest_inventory

def get_dosage_data():
    query = """
    SELECT * FROM dim.dosage_data;
    """
    return db.execute_query(query)

def get_supplement_data():
    query = """
    SELECT * FROM dim.supplements;
    """
    return db.execute_query(query)

#TODO: Add logic to make adjustment to stock levels: add, remove
def make_inventory_adjustment(user_id: int, supplement_id: int, change_amount: int, adjustment_type: str, remarks: str):
    ...