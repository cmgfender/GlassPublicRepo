import pandas as pd
from rapidfuzz import process, fuzz
from tkinter import Tk, filedialog, messagebox, simpledialog
import os

def super_vlookup(df1, df2, key, columns_to_return=None, join_type='left', soft_match=False, threshold=90):
    """
    Perform a VLOOKUP-like operation with optional fuzzy matching.

    Args:
        df1 (DataFrame): The main table.
        df2 (DataFrame): The lookup table.
        key (list): Column(s) to merge on.
        columns_to_return (list, optional): Columns to include from df2. Defaults to all.
        join_type (str): Type of join - 'left', 'right', 'outer', 'inner'. Defaults to 'left'.
        soft_match (bool): Whether to use fuzzy matching. Defaults to False.
        threshold (int): Fuzzy match score threshold (0-100). Defaults to 90.

    Returns:
        DataFrame: Merged DataFrame.
    """
    if columns_to_return:
        df2 = df2[key + columns_to_return]

    if soft_match:
        df2_key = df2[key[0]].tolist()
        df1[key[0]] = df1[key[0]].apply(
            lambda x: process.extractOne(x, df2_key, scorer=fuzz.ratio, score_cutoff=threshold)[0]
            if process.extractOne(x, df2_key, scorer=fuzz.ratio, score_cutoff=threshold)
            else x
        )

    merged_df = pd.merge(df1, df2, on=key, how=join_type)
    return merged_df

def main():
    root = Tk()
    root.withdraw()  # Hide the main Tkinter window

    try:
        # Prompt user to select the first file
        messagebox.showinfo("Select File", "Please select the main table file.")
        file1 = filedialog.askopenfilename(filetypes=[("CSV and Excel files", "*.csv *.xlsx")])
        if not file1:
            raise ValueError("No file selected for the main table.")

        # Prompt user to select the second file
        messagebox.showinfo("Select File", "Please select the lookup table file.")
        file2 = filedialog.askopenfilename(filetypes=[("CSV and Excel files", "*.csv *.xlsx")])
        if not file2:
            raise ValueError("No file selected for the lookup table.")

        # Load the data
        df1 = pd.read_csv(file1) if file1.endswith('.csv') else pd.read_excel(file1)
        df2 = pd.read_csv(file2) if file2.endswith('.csv') else pd.read_excel(file2)

        # Prompt for merge key columns
        key = simpledialog.askstring(
            "Merge Key",
            f"Available columns in the main table:\n{df1.columns.tolist()}\n\n"
            f"Available columns in the lookup table:\n{df2.columns.tolist()}\n\n"
            "Enter the column name(s) to merge on (comma-separated):"
        )
        if not key:
            raise ValueError("No merge key provided.")
        key = [col.strip() for col in key.split(',')]

        # Prompt for columns to return from the second file
        columns_to_return = simpledialog.askstring(
            "Columns to Return",
            f"Available columns in the lookup table:\n{df2.columns.tolist()}\n\n"
            "Enter the column name(s) to return from the lookup table (comma-separated, leave blank for all):"
        )
        if columns_to_return:
            columns_to_return = [col.strip() for col in columns_to_return.split(',')]

        # Prompt for join type
        join_type = simpledialog.askstring("Join Type", "Enter the join type (left, right, outer, inner). Default is 'left':")
        join_type = join_type.strip().lower() if join_type else 'left'

        # Prompt for soft matching
        soft_match = messagebox.askyesno("Soft Matching", "Do you want to use fuzzy matching?")
        threshold = 90
        if soft_match:
            threshold = simpledialog.askinteger(
                "Matching Threshold", "Enter the fuzzy match threshold (0-100, default is 90):", 
                minvalue=0, maxvalue=100
            ) or 90

        # Perform the merge
        result_df = super_vlookup(df1, df2, key, columns_to_return, join_type, soft_match, threshold)

        # Prompt for output file
        output = filedialog.asksaveasfilename(
            defaultextension=".csv", 
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")]
        )
        if not output:
            raise ValueError("No output file specified.")

        # Save the output
        if output.endswith('.csv'):
            result_df.to_csv(output, index=False)
        else:
            result_df.to_excel(output, index=False)

        messagebox.showinfo("Success", f"Results saved to {output}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    main()