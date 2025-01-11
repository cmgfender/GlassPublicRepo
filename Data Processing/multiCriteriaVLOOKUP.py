"""
===========================================================
Script: Multi-Criteria VLOOKUP using Pandas
===========================================================
Purpose:
--------
This script automates the process of performing a multi-criteria VLOOKUP in Excel. 
It reads data from two specified sheets in an Excel file, merges them based on 
common columns (criteria), and saves the merged results to a new Excel file.

Key Features:
-------------
1. Configurable file paths, sheet names, and merge criteria.
2. Supports flexible merge options (`left`, `right`, `inner`, `outer`).
3. Error handling for missing files or columns.
4. User-friendly feedback and previews at each step.
5. Easily adaptable for different datasets and merge operations.

Usage:
------
1. Place the input Excel file in the specified path.
2. Adjust the file path, sheet names, and merge configuration as needed.
3. Run the script to generate the merged data and save it to a new file.

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

# File paths and sheet names: Adjust these to match your data
input_file_path = "data.xlsx"  # Path to the input Excel file
sheet1_name = "Sheet1"  # Name of the first sheet
sheet2_name = "Sheet2"  # Name of the second sheet
output_file_path = "multi_criteria_vlookup.xlsx"  # Output file for the merged data

# Merge configuration: Customize these as needed
merge_how = 'left'  # Merge type: 'left', 'right', 'inner', 'outer'
merge_on = ['Column1', 'Column2']  # Columns used as criteria for merging

# ===========================
# Step 1: Load Data
# ===========================

try:
    print(f"Loading data from {input_file_path}...")
    # Read the specified sheets into pandas DataFrames
    sheet1 = pd.read_excel(input_file_path, sheet_name=sheet1_name)
    sheet2 = pd.read_excel(input_file_path, sheet_name=sheet2_name)
    print(f"Data from '{sheet1_name}' loaded successfully! Here's a preview:")
    print(sheet1.head())  # Preview the first few rows of Sheet1
    print(f"\nData from '{sheet2_name}' loaded successfully! Here's a preview:")
    print(sheet2.head())  # Preview the first few rows of Sheet2
except FileNotFoundError:
    print(f"Error: The file '{input_file_path}' was not found. Please check the file path.")
    exit(1)  # Exit the script if the file is not found
except ValueError as e:
    print(f"Error: {e}. Please check that the sheet names are correct.")
    exit(1)  # Exit if the sheet names are invalid

# ===========================
# Step 2: Merge Data
# ===========================

try:
    print(f"\nMerging data based on criteria: {merge_on}...")
    # Perform the merge operation
    merged_data = pd.merge(
        sheet1,  # First DataFrame
        sheet2,  # Second DataFrame
        how=merge_how,  # Merge type
        on=merge_on  # Columns to merge on
    )
    print("Data merged successfully! Here's a preview of the merged data:")
    print(merged_data.head())  # Preview the first few rows of the merged data
except KeyError as e:
    print(f"Error: Missing required columns for merging - {e}. Please check your merge criteria.")
    exit(1)  # Exit if the merge columns are not found in both sheets

# ===========================
# Step 3: Save Merged Data
# ===========================

try:
    print(f"\nSaving merged data to {output_file_path}...")
    # Save the merged data to an Excel file
    merged_data.to_excel(output_file_path, index=False)
    print(f"Merged data successfully saved as '{output_file_path}'!")
except Exception as e:
    print(f"Error while saving the file: {e}")
    exit(1)  # Exit if an error occurs during file saving

# ===========================
# Summary of Execution
# ===========================

print("\n--- Process Summary ---")
print(f"Input File: {input_file_path}")
print(f"Sheet 1: {sheet1_name}")
print(f"Sheet 2: {sheet2_name}")
print(f"Output File: {output_file_path}")
print(f"Merge Type: {merge_how}")
print(f"Merge Criteria: {merge_on}")
print("Script execution completed successfully!")

# ===========================
# Additional Notes
# ===========================
# - Ensure that the input Excel file and sheets exist.
# - Modify the `merge_on` and `merge_how` variables for different datasets or merge types.
# - This script can be extended to handle additional sheets or more complex merge logic.