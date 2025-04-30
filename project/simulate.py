import requests
import random
from datetime import datetime, timedelta

URL = "http://127.0.0.1:8000/api/transactions/"
API_KEY = "1234"

PAYMENT_TYPES = ["credit", "cash", "gift", "online"]
HEADERS = {
    "Content-Type": "application/json",
    "X-API-KEY": API_KEY
}

def generate_dates(start, end):
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)

start_date = datetime(2025, 4, 18)
end_date = datetime(2025, 4, 29)

for date in generate_dates(start_date, end_date):
    for _ in range(random.randint(3, 6)):  # simulate 3–6 transactions per day
        data = {
            "store": random.randint(1, 3),
            "amount": round(random.uniform(5, 200), 2),
            "payment_type": random.choice(PAYMENT_TYPES),
            "date": date.strftime("%Y-%m-%d"),
            "location_description": "test"
        }

        response = requests.post(URL, json=data, headers=HEADERS)
        print(f"{date.strftime('%Y-%m-%d')} -> {response.status_code} {response.text}")
