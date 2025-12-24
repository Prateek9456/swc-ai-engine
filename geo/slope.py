import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "state_slope_lookup.csv")

SLOPE_DF = pd.read_csv(CSV_PATH)

def slope_from_state(state):
    row = SLOPE_DF[SLOPE_DF["STATE"] == state]
    if row.empty:
        raise ValueError(f"No slope data for {state}")
    return row.iloc[0]["SLOPE_CLASS"]
