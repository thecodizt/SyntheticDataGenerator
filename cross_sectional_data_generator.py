from faker import Faker
import pandas as pd
from categorical_data_generator import generate_categorical_data
from numeric_data_generator import generate_numeric_data
from geographical_data_generator import generate_geographical_data

def generate_cross_sectional_data(num_samples, columns):
    data = {}

    for col in columns:
        col_name = col["name"]
        col_type = col["type"]

        if col_type == "Numeric":
            data[col_name] = generate_numeric_data(num_samples, col["min"], col["max"], col["mean"], col["std_deviation"])
        elif col_type == "Categorical":
            data[col_name] = generate_categorical_data(num_samples, col["categories"])
        elif col_type == "Geographical":
            data[col_name] = generate_geographical_data(num_samples)

    return pd.DataFrame(data)
