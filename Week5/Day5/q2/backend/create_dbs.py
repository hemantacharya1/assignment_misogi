import sqlite3
import pandas as pd
import os

DATA_PATH = "./data"
DB_PATH = "./db"

def create_blinkit_db():
    df = pd.read_csv(os.path.join(DATA_PATH, "blinkit.csv"))
    conn = sqlite3.connect(os.path.join(DB_PATH, "blinkit.db"))
    df.to_sql("product", conn, if_exists="replace", index=False)
    conn.close()

def create_zepto_db():
    df = pd.read_csv(os.path.join(DATA_PATH, "zepto.csv"), encoding="windows-1252")
    conn = sqlite3.connect(os.path.join(DB_PATH, "zepto.db"))
    df.to_sql("product", conn, if_exists="replace", index=False)
    conn.close()

def create_bigbasket_db():
    df = pd.read_csv(os.path.join(DATA_PATH, "bigbasket.csv"))
    conn = sqlite3.connect(os.path.join(DB_PATH, "bigbasket.db"))
    df.to_sql("product", conn, if_exists="replace", index=False)
    conn.close()

if __name__ == "__main__":
    os.makedirs(DB_PATH, exist_ok=True)
    create_blinkit_db()
    create_zepto_db()
    create_bigbasket_db()
    print("✅ All databases created.")
