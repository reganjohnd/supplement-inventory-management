from services.inventory_service import update_inventory
from services.alerts_service import generate_purchase_alerts
import pandas as pd
from pandas import Timestamp




def main():
    current_date = pd.Timestamp('2025-03-23')
    inventory = update_inventory(current_date)
    generate_purchase_alerts(inventory)
    # print(alerts)

if __name__ == "__main__":
    main()