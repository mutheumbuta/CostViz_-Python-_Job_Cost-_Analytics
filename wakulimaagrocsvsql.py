import pandas as pd
import mysql.connector
import logging

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

CSV_FILE = "wakulimaagro_cleaned.csv"

DB_CONFIG = {
    "host": "mutheumbuta",
    "user": "root",
    "password": "Mbuta@9989",
    "database": "wakulima_agro_db"
}

TABLE_NAME = "wakulima agro job costing"

def connect_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        logging.info("Connected to MySQL database")
        return conn
    except Exception as e:
        logging.error(f"Database connection failed: {e}")
        return None

def create_table(cursor):
    query = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        item_code VARCHAR(100),
        product_name VARCHAR(255),
        category VARCHAR(100),
        quantity FLOAT,
        uom VARCHAR(50),
        cost_kes DECIMAL(10,2),
        production_cost DECIMAL(12,2),
        currency VARCHAR(10)
    )
    """
    cursor.execute(query)

def upload_csv(conn):
    try:
        df = pd.read_csv(CSV_FILE)

        cursor = conn.cursor()
        create_table(cursor)

        insert_query = f"""
        INSERT INTO {TABLE_NAME}
        (item_code, product_name, category, quantity, uom, cost, production_cost, currency)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """

        for _, row in df.iterrows():
            cursor.execute(insert_query, tuple(row))

        conn.commit()
        logging.info("CSV uploaded successfully")

    except Exception as e:
        logging.error(f"Upload failed: {e}")

def run_queries(conn):
    cursor = conn.cursor()

    queries = {
        "Total Production Cost":
        "SELECT SUM(production_cost) FROM products",

        "Most Expensive Products":
        "SELECT product_name, production_cost FROM products ORDER BY production_cost DESC LIMIT 5",

        "Products Per Category":
        "SELECT category, COUNT(*) FROM products GROUP BY category",

        "Average Cost":
        "SELECT AVG(cost) FROM products"
    }

    for title, query in queries.items():
        cursor.execute(query)
        result = cursor.fetchall()
        print(f"\n{title}")
        for r in result:
            print(r)

def main():
    conn = connect_db()

    if conn:
        upload_csv(conn)
        run_queries(conn)
        conn.close()
        logging.info("Process completed")

if __name__ == "__main__":
    main()
