import pandas as pd
import numpy as np
from faker import Faker
from numeric_data_generator import generate_numeric_data
from categorical_data_generator import generate_categorical_data

fake = Faker()

def generate_time_series_data(num_time_points, columns, start_date=None, end_date=None):
    data = {}

    if start_date and end_date:
        date_range = pd.date_range(start=start_date, end=end_date, periods=num_time_points)
        data['Date'] = date_range
    else:
        data['Date'] = pd.date_range(start=pd.Timestamp.today(), periods=num_time_points)

    for col in columns:
        col_name = col["name"]
        col_type = col["type"]

        if col_type == "Numeric":
            # Check if the column has seasonality and trend parameters
            if "seasonality" in col and "trend" in col:
                data[col_name] = generate_numeric_data_with_seasonality_and_trend(
                    num_time_points, col["min"], col["max"], col["mean"], col["std_deviation"],
                    col["seasonality"], col["trend"]
                )
            else:
                data[col_name] = generate_numeric_data(num_time_points, col["min"], col["max"], col["mean"], col["std_deviation"])
        elif col_type == "Categorical":
            data[col_name] = generate_categorical_data(num_time_points)

    return pd.DataFrame(data)

def generate_numeric_data_with_seasonality_and_trend(num_samples, min_value, max_value, mean, std_deviation, seasonality, trend):
    # Add seasonality and trend to the generated numeric data
    base_data = generate_numeric_data(num_samples, min_value, max_value, mean, std_deviation)
    
    # Apply seasonality and trend
    seasonal_component = generate_seasonal_component(num_samples, seasonality)
    trend_component = generate_trend_component(num_samples, trend)
    
    # Combine components
    final_data = [base + seasonal + trend for base, seasonal, trend in zip(base_data, seasonal_component, trend_component)]
    
    return final_data

def generate_seasonal_component(num_samples, seasonality):
    # Implement your logic for generating seasonal component
    amplitude = seasonality.get("amplitude", 1.0)
    frequency = seasonality.get("frequency", 1.0)
    seasonal_component = [amplitude * np.sin(2 * np.pi * frequency * i / num_samples) for i in range(num_samples)]
    
    return seasonal_component

def generate_trend_component(num_samples, trend):
    slope = trend.get("slope", 0.0)
    trend_component = [slope * i for i in range(num_samples)]
    
    return trend_component
