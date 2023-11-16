import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from faker import Faker
from cross_sectional_data_generator import generate_cross_sectional_data
from time_series_data_generator import generate_time_series_data
from numeric_data_generator import generate_numeric_data
from categorical_data_generator import generate_categorical_data

# Function to generate data for a specific table based on its type
def generate_table_data(table_name, table_type, num_records, num_time_points, columns, start_date=None, end_date=None):
    if table_type == "Cross-Sectional":
        return generate_cross_sectional_data(num_records, columns)
    elif table_type == "Time Series":
        return generate_time_series_data(num_time_points, columns, start_date, end_date)

# Function to generate Plotly chart based on the selected data
def generate_plot(table_data, selected_column):
    if pd.api.types.is_numeric_dtype(table_data[selected_column]):
        # For numeric columns, generate a line plot
        fig = px.line(table_data, x=table_data.index, y=selected_column, title=f"{selected_column} - Line Plot")
    elif pd.api.types.is_datetime64_any_dtype(table_data[selected_column]):
        # For date columns, generate a frequency plot
        fig = px.histogram(table_data, x=selected_column, title=f"{selected_column} - Frequency Plot")
    else:
        # For categorical columns, generate a bar chart
        fig = px.bar(table_data, x=table_data.index, y=selected_column, title=f"{selected_column} - Bar Chart")

    st.plotly_chart(fig)

# Main function to run the Streamlit app
def main():
    st.title("Synthetic Data Generator")

    # Get the number of tables from the user
    num_tables = st.number_input("Enter the number of tables", min_value=1, step=1, value=1, key="num_tables")

    # Initialize table information
    table_info = []

    # Gather information for each table
    for i in range(num_tables):
        st.header(f"Table {i+1} Configuration")

        # Get table name and type with unique key
        table_name = st.text_input(f"Enter table name {i+1}:", key=f"table_name_{i}")
        table_type = st.radio("Select table type:", ("Cross-Sectional", "Time Series"), key=f"table_type_{i}")

        # Get parent-child relationships
        if i > 0:
            st.subheader("Define Relationships:")
            parent_table = st.selectbox("Select parent table:", [info['name'] for info in table_info], key=f"parent_table_{i}")
            child_table = table_name
            table_info[i - 1]['child'] = child_table

        # Get column information with unique key
        st.subheader("Define Table Fields:")
        num_columns = st.number_input("Enter the number of columns", min_value=1, step=1, value=1, key=f"num_columns_{i}")

        columns = []
        for j in range(num_columns):
            # Provide a unique key for each text_input and radio widget
            column_name = st.text_input(f"Enter column name {j + 1}:", key=f"column_name_{i}_{j}")
            column_type = st.radio(f"Select column type for {column_name}:", ("Numeric", "Categorical", "Geographical" if table_type == "Cross-Sectional" else "Date"), key=f"column_type_{i}_{j}")

            # For foreign keys
            if st.checkbox(f"Is {column_name} a foreign key?", key=f"foreign_key_{i}_{j}"):
                foreign_key_table = st.selectbox(f"Select the foreign key table for {column_name}:", [info['name'] for info in table_info], key=f"foreign_key_table_{i}_{j}")
                columns.append({"name": column_name, "type": column_type, "foreign_key": foreign_key_table})
            elif column_type == "Date" and table_type != "Time Series":
                st.warning("Date data is only supported for Time Series tables.")
            else:
                # Add more controls based on column type
                if column_type == "Numeric":
                    min_value = st.number_input(f"Enter minimum value for {column_name}:", value=0.0, key=f"min_value_{i}_{j}")
                    max_value = st.number_input(f"Enter maximum value for {column_name}:", value=100.0, key=f"max_value_{i}_{j}")
                    mean_value = st.number_input(f"Enter mean value for {column_name}:", value=50.0, key=f"mean_value_{i}_{j}")
                    std_deviation = st.number_input(f"Enter standard deviation for {column_name}:", value=10.0, key=f"std_deviation_{i}_{j}")
                    
                    # Trend and Seasonality options
                    with st.expander(f"Options for Numeric Column {column_name}"):
                        col_seasonality = st.checkbox(f"Add Seasonality to {column_name}?", key=f"col_seasonality_{i}_{j}")
                        col_trend = st.checkbox(f"Add Trend to {column_name}?", key=f"col_trend_{i}_{j}")

                        if col_seasonality:
                            amplitude = st.number_input(f"Enter Seasonality Amplitude for {column_name}:", key=f"amplitude_{i}_{j}")
                            frequency = st.number_input(f"Enter Seasonality Frequency for {column_name}:", key=f"frequency_{i}_{j}")
                        else:
                            amplitude = 1.0
                            frequency = 1.0

                        if col_trend:
                            slope = st.number_input(f"Enter Trend Slope for {column_name}:", key=f"slope_{i}_{j}")
                        else:
                            slope = 0.0

                    columns.append({"name": column_name, "type": column_type, "foreign_key": None, 
                                    "min": min_value, "max": max_value, "mean": mean_value, "std_deviation": std_deviation,
                                    "seasonality": {"amplitude": amplitude, "frequency": frequency},
                                    "trend": {"slope": slope}})
                elif column_type == "Categorical":
                    columns.append({"name": column_name, "type": column_type, "foreign_key": None})
                elif column_type == "Geographical":
                    columns.append({"name": column_name, "type": column_type, "foreign_key": None})
                else:
                    columns.append({"name": column_name, "type": column_type, "foreign_key": None})

        # Get the number of records for the table with unique key
        num_records = st.number_input(f"Enter the number of records for {table_name}", min_value=1, step=1, value=100, key=f"num_records_{i}")

        # Get start and end dates only if the table type is Time Series
        start_date = None
        end_date = None
        if table_type == "Time Series":
            start_date = st.date_input(f"Enter the start date for {table_name} (YYYY-MM-DD):", key=f"start_date_{i}")
            end_date = st.date_input(f"Enter the end date for {table_name} (YYYY-MM-DD):", key=f"end_date_{i}")

        table_info.append({"name": table_name, "type": table_type, "columns": columns, "parent": None, "child": None, "num_records": num_records, "start_date": start_date, "end_date": end_date})

    # Generate and display synthetic data for each table
    st.subheader("Generated Data Preview:")

    for info in table_info:
        st.subheader(f"Table: {info['name']}")
        table_data = generate_table_data(info['name'], info['type'], info['num_records'], num_records, info['columns'], start_date=info.get('start_date'), end_date=info.get('end_date'))

        st.dataframe(table_data)

        # Visualize Data
        st.subheader("Visualize Data:")
        selected_table = st.selectbox("Select a table for visualization:", [info['name'] for info in table_info], key=f"selected_table_{info['name']}")
        selected_column = st.selectbox("Select a column for visualization:", table_data.columns, key=f"selected_column_{info['name']}")

        generate_plot(table_data, selected_column)

        # Download button for each table
        csv_download = table_data.to_csv(index=False).encode('utf-8')
        st.download_button(f"Download {info['name']} as CSV", csv_download, f'{info["name"]}_data.csv', 'text/csv')

if __name__ == "__main__":
    main()
