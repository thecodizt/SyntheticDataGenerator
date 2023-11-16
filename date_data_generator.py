import pandas as pd

def generate_date_data(num_samples, min_date, max_date):
    return pd.date_range(min_date, max_date, periods=num_samples)
