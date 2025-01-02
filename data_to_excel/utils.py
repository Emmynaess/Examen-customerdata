import unicodedata
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker("sv_SE")

def clean_string(s):
    s = unicodedata.normalize('NFKD', s)
    s = s.encode('ascii', 'ignore').decode('ascii')
    s = s.lower()
    s = s.replace(' ', '')
    return s

def generate_swedish_phone_number():
    area_code = random.choice(["70", "72", "73", "76"])
    first_part = random.randint(100, 999)
    second_part = random.randint(10, 99)
    third_part = random.randint(10, 99)
    return f"+46 {area_code}-{first_part} {second_part} {third_part}"

def generate_valid_purchase_date(base_date=None):
    today = datetime.today().date()
    if base_date is None:
        base_date = fake.date_between(start_date='-1y', end_date=today)
    
    time_offset = timedelta(days=random.randint(0, 2), hours=random.randint(0, 23))
    adjusted_date = datetime.combine(base_date, datetime.min.time()) + time_offset
    
    if adjusted_date.date() > today:
        adjusted_date = adjusted_date - timedelta(days=1)
    
    return adjusted_date.strftime('%Y-%m-%d')