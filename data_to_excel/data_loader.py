import pandas as pd
import os
import logging

def load_products_from_csv(filename):
    try:
        filepath = os.path.join(os.path.dirname(__file__), filename)
        products_df = pd.read_csv(filepath)
        return products_df.to_dict(orient="records")
    except Exception as e:
        logging.error(f"Failed to load products from {filename}: {e}")
        return []
