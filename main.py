import streamlit as st
from cross_sectional_data_generator import generate_cross_sectional_data
from time_series_data_generator import generate_time_series_data

# Function to generate data for a specific table based on its type
def generate_table_data(table_name, table_type, num_records, num_time_points, columns):
    if table_type == "Cross-Sectional":
        return generate_cross_sectional_data(num_records, columns)
    elif table_type == "Time Series":
        return generate_time_series_data(num_time_points, columns)

# Main function to run the Streamlit app
def main():
    st.title("Synthetic Data Generator")

    # Get the number of tables from the user
    num_tables = st.number_input("Enter the number of tables", min_value=1, step=1, value=1)

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
            table_info[i]['parent'] = parent_table
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
            if st.checkbox(f"Is {column_name} a foreign key?", key=f"checkbox_foreign_key_{i}_{j}"):
                foreign_key_table = st.selectbox(f"Select the foreign key table for {column_name}:", [info['name'] for info in table_info], key=f"foreign_key_table_{i}_{j}")
                columns.append({"name": column_name, "type": column_type, "foreign_key": foreign_key_table})
            elif column_type == "Date" and table_type != "Time Series":
                st.warning("Date data is only supported for Time Series tables.")
            else:
                # Add more controls based on column type
                if column_type == "Numeric":
                    min_value = st.number_input(f"Enter minimum value for {column_name}:", value=0.0, key=f"min_{i}_{j}")
                    max_value = st.number_input(f"Enter maximum value for {column_name}:", value=100.0, key=f"max_{i}_{j}")
                    mean_value = st.number_input(f"Enter mean value for {column_name}:", value=50.0, key=f"mean_{i}_{j}")
                    std_deviation = st.number_input(f"Enter standard deviation for {column_name}:", value=10.0, key=f"std_dev_{i}_{j}")
                    columns.append({"name": column_name, "type": column_type, "foreign_key": None, "min": min_value, "max": max_value, "mean": mean_value, "std_deviation": std_deviation})
                elif column_type == "Categorical":
                    columns.append({"name": column_name, "type": column_type, "foreign_key": None})
                elif column_type == "Geographical":
                    columns.append({"name": column_name, "type": column_type, "foreign_key": None})
                else:
                    columns.append({"name": column_name, "type": column_type, "foreign_key": None})

        # Get the number of records for the table with unique key
        num_records = st.number_input(f"Enter the number of records for {table_name}", min_value=1, step=1, value=100, key=f"num_records_{i}")

        table_info.append({"name": table_name, "type": table_type, "columns": columns, "parent": None, "child": None, "num_records": num_records})

    # Generate and display synthetic data for each table
    st.subheader("Generated Data Preview:")

    for info in table_info:
        st.subheader(f"Table: {info['name']}")
        table_data = generate_table_data(info['name'], info['type'], info['num_records'], 30, info['columns'])
        st.dataframe(table_data)

        # Download button for each table
        csv_download = table_data.to_csv(index=False).encode('utf-8')
        st.download_button(f"Download {info['name']} as CSV", csv_download, f'{info["name"]}_data.csv', 'text/csv', key=f"download_button_{info['name']}")

if __name__ == "__main__":
    main()
