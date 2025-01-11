"""
===========================================================
Script: Excel Pivot Table Generator
===========================================================
Purpose:
--------
This script automates the process of generating a pivot table from an Excel dataset. 
It reads sales data from a specified input file, summarizes the data based on 
configurable criteria (e.g., region, product, and sales values), and saves the resulting 
pivot table to a new Excel file.

Key Features:
-------------
1. Configurable file paths for input and output.
2. Flexible pivot table setup with customizable:
   - Values: The data column to aggregate.
   - Index: The rows in the pivot table.
   - Columns: The columns in the pivot table.
   - Aggregation Function: The method for summarizing data (e.g., sum, average).
   - Fill Value: Replacement for missing or empty cells.
3. Error handling to manage file-related issues or missing data.
4. Clear feedback to the user during each step of execution.
5. Easily distributable and reusable by adjusting configuration variables.

Usage:
------
1. Place the input Excel file in the specified path.
2. Adjust the file path and pivot table settings as needed.
3. Run the script to generate the pivot table and save it to a new file.

Dependencies:
-------------
- Python 3.x
- pandas library (install via `pip install pandas`)
- openpyxl library (install via `pip install openpyxl` for Excel support)

===========================================================
"""

# Import necessary library
import pandas as pd  # pandas is used for data manipulation and analysis

# ===========================
# Configuration Section
# ===========================

# File paths: Adjust these to match your directory and file names
input_file_path = "sales_data.xlsx"  # Input file containing raw sales data
output_file_path = "pivot_table.xlsx"  # Output file for the pivot table

# Pivot table configuration: Customize these to match your dataset and analysis needs
pivot_values = 'Sales'  # Column to aggregate (e.g., 'Sales', 'Revenue')
pivot_index = 'Region'  # Rows in the pivot table (e.g., 'Region', 'Customer')
pivot_columns = 'Product'  # Columns in the pivot table (e.g., 'Product', 'Category')
pivot_aggfunc = 'sum'  # Aggregation function (e.g., 'sum', 'mean', 'count')
pivot_fill_value = 0  # Value to replace missing data in the pivot table

# ===========================
# Step 1: Load Excel Data
# ===========================

try:
    print(f"Loading data from {input_file_path}...")
    # Read the input Excel file into a pandas DataFrame
    data = pd.read_excel(input_file_path)
    print("Data loaded successfully! Here are the first few rows of your dataset:")
    print(data.head())  # Display the first few rows for confirmation
except FileNotFoundError:
    print(f"Error: The file '{input_file_path}' was not found. Please check the file path and try again.")
    exit(1)  # Exit the script with an error code if the file is not found

# ===========================
# Step 2: Create Pivot Table
# ===========================

try:
    print("Creating pivot table...")
    # Generate the pivot table using the specified configurations
    pivot_table = pd.pivot_table(
        data,  # Source data
        values=pivot_values,  # Data to aggregate
        index=pivot_index,  # Rows in the pivot table
        columns=pivot_columns,  # Columns in the pivot table
        aggfunc=pivot_aggfunc,  # Aggregation function
        fill_value=pivot_fill_value  # Fill missing data with this value
    )
    print("Pivot table created successfully! Here's a preview:")
    print(pivot_table.head())  # Display the first few rows of the pivot table
except KeyError as e:
    print(f"Error: Missing required column in the data - {e}. Please check your pivot table configuration.")
    exit(1)  # Exit if required columns are missing

# ===========================
# Step 3: Save Pivot Table
# ===========================

try:
    print(f"Saving pivot table to {output_file_path}...")
    # Save the pivot table to an Excel file
    pivot_table.to_excel(output_file_path)
    print(f"Pivot table successfully saved as '{output_file_path}'!")
except Exception as e:
    print(f"Error while saving the pivot table: {e}")
    exit(1)  # Exit if an error occurs during file saving

# ===========================
# Summary of Execution
# ===========================

print("\n--- Process Summary ---")
print(f"Input File: {input_file_path}")
print(f"Output File: {output_file_path}")
print(f"Pivot Table Configurations: ")
print(f"    Values: {pivot_values}")
print(f"    Index: {pivot_index}")
print(f"    Columns: {pivot_columns}")
print(f"    Aggregation Function: {pivot_aggfunc}")
print(f"    Fill Value: {pivot_fill_value}")
print("Script execution completed successfully!")

# ===========================
# Additional Notes
# ===========================
# - Ensure that the input Excel file exists and contains the necessary columns.
# - Modify the pivot table configurations as needed for different analyses.
# - This script can be extended further to handle multiple pivot tables or automate email distribution.