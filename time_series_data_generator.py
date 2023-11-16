from faker import Faker
import pandas as pd

def generate_time_series_data(num_time_points, columns):
    data = {}

    for col in columns:
        col_name = col["name"]
        col_type = col["type"]

        if col_type == "Numeric":
            data[col_name] = generate_numeric_data(num_time_points, col["min"], col["max"], col["mean"], col["std_deviation"])
        elif col_type == "Categorical":
            data[col_name] = generate_categorical_data(num_time_points, col["categories"])

    return pd.DataFrame(data)
