import pandas as pd
import requests
import logging
import os
import time
from dotenv import load_dotenv

load_dotenv()

INPUT_FILE = "wakulima_agro_limited.csv"
OUTPUT_FILE = "wakulimaagro_cleaned.csv"

API_KEY = os.getenv("EXCHANGE_API_KEY")

DEFAULT_USD = float(os.getenv("DEFAULT_USD_KES", 150))
DEFAULT_EUR = float(os.getenv("DEFAULT_EUR_KES", 160))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# function to retry API requests with exponential backoff
def retry_request(url, retries=3, delay=3):
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.json()
            logging.warning(f"API attempt {attempt+1} failed: {response.status_code}")
        except Exception as e:
            logging.warning(f"Attempt {attempt+1} error: {e}")
        time.sleep(delay)
    return None

# exchange rate fetcher with retry and fallback
def get_rates():
    if not API_KEY:
        logging.warning("Missing API key, using default rates")
        return DEFAULT_USD, DEFAULT_EUR

    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"
    data = retry_request(url)

    if data:
        try:
            usd_kes = data["conversion_rates"]["KES"]
            eur_kes = usd_kes / data["conversion_rates"]["EUR"]
            logging.info("Live exchange rates loaded successfully")
            return usd_kes, eur_kes
        except Exception:
            logging.warning("Malformed API response, using defaults")

    return DEFAULT_USD, DEFAULT_EUR

# validation function to ensure required columns are present
def validate(df):
    required = ["ITEM CODE", "PRODUCT NAME", "QUANTITY", "COST", "CURRENCY"]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

# conversion function to convert costs to KES based on currency
def convert(row, usd, eur):
    currency = str(row["CURRENCY"]).upper()

    if currency == "USD":
        return row["COST"] * usd
    elif currency in ["EUR", "EURO"]:
        return row["COST"] * eur
    else:
        return row["COST"]

# function to load excel with fallback for different engines
def load_excel(file):
    try:
        return pd.read_excel(file, engine="openpyxl")
    except Exception:
        return pd.read_excel(file, engine="xlrd")

# main processing function that orchestrates the entire workflow
def process():
    try:
        logging.info("Loading Excel file...")

        df = load_excel(INPUT_FILE)

        validate(df)

        df = df.dropna(subset=["ITEM CODE", "PRODUCT NAME", "COST"])

        usd, eur = get_rates()

        df["COST_KES"] = df.apply(lambda r: convert(r, usd, eur), axis=1)

        grouped = df.groupby(
            ["ITEM CODE", "PRODUCT NAME", "CATEGORY", "U.O.M"],
            as_index=False
        ).agg({
            "QUANTITY": "sum",
            "COST_KES": "mean"
        })

        grouped["TOTAL_COST_OF_PRODUCTION"] = grouped["QUANTITY"] * grouped["COST_KES"]

        total = grouped["TOTAL_COST_OF_PRODUCTION"].sum()

        logging.info(f"TOTAL COST OF PRODUCTION: {total:,.2f} KES")

        grouped["CURRENCY"] = "KES"

        grouped.to_excel(OUTPUT_FILE, index=False)

        logging.info(f"Cleaned file saved successfully: {OUTPUT_FILE}")

    except FileNotFoundError:
        logging.error("Input file not found.")
    except ValueError as e:
        logging.error(f"Validation error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    process()
