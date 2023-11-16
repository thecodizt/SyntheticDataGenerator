import pandas as pd
import random
from faker import Faker

fake = Faker()

def generate_cross_sectional_data(num_samples, columns):
    data = {}
    for col in columns:
        col_name = col["name"]
        col_type = col["type"]

        if col_type == "Numeric":
            min_val = col["min"]
            max_val = col["max"]
            data[col_name] = [random.uniform(min_val, max_val) for _ in range(num_samples)]
        elif col_type == "Categorical":
            data[col_name] = [fake.word() for _ in range(num_samples)]
        elif col_type == "Date":
            min_date = col["min"]
            max_date = col["max"]
            data[col_name] = [fake.date_time_between_dates(min_date, max_date) for _ in range(num_samples)]
        elif col_type == "Geographical":
            data[col_name] = [fake.local_latlng(country_code='US', coords_only=True) for _ in range(num_samples)]
        else:
            raise ValueError(f"Unsupported column type: {col_type}")

    return pd.DataFrame(data)
