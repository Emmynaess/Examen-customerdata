import pandas as pd
import random
from faker import Faker
from datetime import datetime
from utils import clean_string, generate_swedish_phone_number, generate_valid_purchase_date
from data_loader import load_products_from_csv
from coordinate_utils import generate_coordinates, get_address_from_coordinates
from config import AZURE_MAPS_API_KEY
from error_injector import introduce_realistic_errors
import math

fake = Faker("sv_SE")

def generate_data(rows=10, max_retries=10):
    domains = ["hotmail.com", "gmail.com", "outlook.com", "live.com", "icloud.com"]
    products = load_products_from_csv("products.csv")

    data = []

    for i in range(rows):
        first_name = fake.first_name()
        last_name = fake.last_name()
        birthdate = fake.date_of_birth(minimum_age=18, maximum_age=70).strftime('%Y-%m-%d')
        phone = generate_swedish_phone_number()
        email = f"{clean_string(first_name)}.{clean_string(last_name)}@{random.choice(domains)}"
        customer_category = random.choice(["Private", "Business"])

        for attempt in range(max_retries):
            lat, lon = generate_coordinates()
            street, postcode, city, municipality = get_address_from_coordinates(lat, lon, AZURE_MAPS_API_KEY)
            if street != "No Street" and postcode != "No Postcode" and city != "No City" and municipality != "No Municipality":
                break
        else:
            street, postcode, city, municipality = "Fallback Street", "Fallback Postcode", "Fallback City", "Fallback Municipality"

        purchase_count = random.randint(1, 2)
        base_date = fake.date_between(start_date='-1y', end_date=datetime.today().date())

        for _ in range(purchase_count):
            purchase_date = generate_valid_purchase_date(base_date)
            product = random.choice(products) 
            quantity = random.randint(1, 5)
            total_amount = product["price"] * quantity 

            data.append({
                "First Name": first_name,
                "Last Name": last_name,
                "Birthdate": birthdate,
                "Phone": phone,
                "Email": email,
                "Customer Category": customer_category,
                "Streetname": street,
                "Postcode": postcode,
                "City": city,
                "Municipality": municipality,
                "Purchase Date": purchase_date,
                "Product": product["productName"], 
                "ProductID": product["productID"], 
                "Quantity": quantity,
                "Price per Item": product["price"],
                "Total Amount": total_amount
            })

    df = pd.DataFrame(data)
    return df

def generate_and_corrupt_data(rows=10):
    df = generate_data(rows)
    df_with_errors = introduce_realistic_errors(df, error_probability=0.05)
    return df_with_errors