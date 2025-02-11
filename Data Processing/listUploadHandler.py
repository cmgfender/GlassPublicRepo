"""
================================================================================
PYTHON SCRIPT: process_event_list.py

A COMPREHENSIVE SCRIPT FOR FORMATTING EVENT LIST UPLOADS INTO A CRM

FEATURES:
---------
1. Reads an input CSV file from the user
2. Splits full names into first and last names (if needed)
3. Checks email validity with a simple regex
4. Normalizes/validates the data (e.g. marking invalid emails)
5. Writes the processed data out to a new CSV file

--------------------------------------------------------------------------------
INSTRUCTIONS TO RUN:
1. INSTALL PYTHON (IF NEEDED):
   - Go to https://www.python.org/downloads/
   - Download and install Python 3.x for your operating system (Windows, macOS, or Linux).
   - Ensure Python is correctly installed by opening a terminal/command prompt and typing:
       python --version
     which should display the installed Python version.

2. SAVE THIS SCRIPT:
   - Copy and paste this entire code block into a file named "process_event_list.py"
     (or any other name you prefer, but remember to adjust accordingly).

3. OPTIONAL: CREATE AND ACTIVATE A VIRTUAL ENVIRONMENT
   - (Recommended for cleaner project setup, but not strictly necessary for simple scripts)
   - Windows Example:
       python -m venv venv
       venv\Scripts\activate
   - macOS/Linux Example:
       python3 -m venv venv
       source venv/bin/activate

4. RUN THE SCRIPT:
   - From a terminal/command prompt in the directory containing "process_event_list.py", type:
       python process_event_list.py
   - If using Python 3 on certain systems, you may need:
       python3 process_event_list.py

5. FOLLOW THE PROMPTS:
   - You will be asked to specify:
       - The input CSV file path
       - Confirmation or override of which columns represent 'Full Name', 'First Name', 'Last Name', and 'Email'
       - The desired output CSV file path

6. CHECK THE OUTPUT:
   - Open the output CSV file (default: "processed_event_list.csv")
   - Verify that data has been correctly split into first name, last name, validated email, etc.
================================================================================
"""

import csv
import re
import os

def is_valid_email(email: str) -> bool:
    """
    Checks if an email address is valid using a simple regex.
    NOTE: This is a basic pattern. For more robust checks, you may want a more
    comprehensive regex or a dedicated validation library.
    """
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return True if re.match(email_regex, email) else False

def split_name(full_name: str):
    """
    Splits a full name string into first name and last name.
    For simple cases, we'll split by the first space.
    If there's only one word, we'll treat it as first name only.
    """
    # Strip leading/trailing whitespace
    full_name = full_name.strip()

    # Handle empty or None values
    if not full_name:
        return ("", "")
    
    # Split on spaces
    parts = full_name.split()
    
    # If there's only one name (e.g., "Madonna"), treat it as first name only
    if len(parts) == 1:
        return (parts[0], "")
    
    # Return the first word as first name, and the remaining words as last name
    # e.g. "John James Smith" => first="John", last="James Smith"
    return (parts[0], " ".join(parts[1:]))

def get_user_input(prompt: str, default_value: str = "") -> str:
    """
    Helper function to get user input with a prompt.
    Provides a default value if user just presses Enter.
    """
    user_in = input(f"{prompt} [default: {default_value}]: ").strip()
    return user_in if user_in else default_value

def process_event_list():
    """
    Main function to:
    1. Prompt user for CSV file path
    2. Read CSV file
    3. Detect columns (Full Name, First Name, Last Name, Email)
    4. Split/transform/validate data
    5. Write output to new CSV
    """
    # -------------------------------------------------------------------
    # 1. GET INPUT CSV FILE PATH FROM THE USER
    # -------------------------------------------------------------------
    input_file_path = get_user_input(
        prompt="Enter the path of your event list CSV file",
        default_value="event_list.csv"
    )
    
    # Check if file exists
    if not os.path.exists(input_file_path):
        print(f"Error: The file '{input_file_path}' does not exist.")
        return

    # -------------------------------------------------------------------
    # 2. READ THE CSV FILE
    # -------------------------------------------------------------------
    processed_data = []
    with open(input_file_path, "r", encoding="utf-8-sig") as infile:
        reader = csv.DictReader(infile)
        
        # Possible columns we want to detect
        possible_name_columns = ["Name", "Full Name", "Participant Name"]
        possible_first_name_columns = ["First Name", "FName", "FirstName"]
        possible_last_name_columns = ["Last Name", "LName", "LastName"]
        possible_email_columns = ["Email", "E-mail", "Email Address"]
        
        # Variables to hold detected column names
        detected_full_name_col = None
        detected_first_name_col = None
        detected_last_name_col = None
        detected_email_col = None
        
        # Try to detect column names automatically
        for col in reader.fieldnames:
            clean_col = col.strip().lower()
            if clean_col in [x.lower() for x in possible_name_columns]:
                detected_full_name_col = col
            if clean_col in [x.lower() for x in possible_first_name_columns]:
                detected_first_name_col = col
            if clean_col in [x.lower() for x in possible_last_name_columns]:
                detected_last_name_col = col
            if clean_col in [x.lower() for x in possible_email_columns]:
                detected_email_col = col
        
        # Let the user confirm or override
        if detected_full_name_col:
            user_full_name_col = get_user_input(
                f"Detected '{detected_full_name_col}' as the Full Name column. "
                "Press Enter to confirm or type an alternative column name",
                detected_full_name_col
            )
            detected_full_name_col = user_full_name_col
        else:
            detected_full_name_col = get_user_input(
                "Could not detect a 'Full Name' column. "
                "Enter the column name if you have one",
                ""
            )
        
        if detected_first_name_col:
            user_first_name_col = get_user_input(
                f"Detected '{detected_first_name_col}' as the First Name column. "
                "Press Enter to confirm or type an alternative column name",
                detected_first_name_col
            )
            detected_first_name_col = user_first_name_col
        else:
            detected_first_name_col = get_user_input(
                "Could not detect a 'First Name' column. "
                "Enter the column name if you have one",
                ""
            )
        
        if detected_last_name_col:
            user_last_name_col = get_user_input(
                f"Detected '{detected_last_name_col}' as the Last Name column. "
                "Press Enter to confirm or type an alternative column name",
                detected_last_name_col
            )
            detected_last_name_col = user_last_name_col
        else:
            detected_last_name_col = get_user_input(
                "Could not detect a 'Last Name' column. "
                "Enter the column name if you have one",
                ""
            )
        
        if detected_email_col:
            user_email_col = get_user_input(
                f"Detected '{detected_email_col}' as the Email column. "
                "Press Enter to confirm or type an alternative column name",
                detected_email_col
            )
            detected_email_col = user_email_col
        else:
            detected_email_col = get_user_input(
                "Could not detect an 'Email' column. "
                "Enter the column name if you have one",
                ""
            )
        
        # -------------------------------------------------------------------
        # 3. PROCESS EACH ROW
        # -------------------------------------------------------------------
        for row in reader:
            first_name = ""
            last_name = ""
            
            # If we have a dedicated first name column
            if detected_first_name_col and detected_first_name_col in row:
                first_name = row[detected_first_name_col].strip()
            
            # If we have a dedicated last name column
            if detected_last_name_col and detected_last_name_col in row:
                last_name = row[detected_last_name_col].strip()
            
            # If first/last are still missing, try full name
            if (not first_name or not last_name) and detected_full_name_col and detected_full_name_col in row:
                name_string = row[detected_full_name_col]
                split_first, split_last = split_name(name_string)
                if not first_name:
                    first_name = split_first
                if not last_name:
                    last_name = split_last
            
            # Extract and validate email
            email = ""
            if detected_email_col and detected_email_col in row:
                email = row[detected_email_col].strip()
            
            email_valid = is_valid_email(email) if email else False
            
            processed_contact = {
                "First Name": first_name,
                "Last Name": last_name,
                "Email": email,
                "Email Valid?": "Yes" if email_valid else "No"
            }
            
            # You can copy additional columns if you wish, for example:
            # processed_contact["Company"] = row.get("Company", "").strip()
            
            processed_data.append(processed_contact)
    
    # -------------------------------------------------------------------
    # 4. WRITE THE OUTPUT TO A NEW CSV
    # -------------------------------------------------------------------
    output_file_path = get_user_input(
        prompt="Enter the desired output CSV file name/path",
        default_value="processed_event_list.csv"
    )
    
    with open(output_file_path, "w", newline="", encoding="utf-8") as outfile:
        # Determine fieldnames from the first record's keys
        if processed_data:
            fieldnames = list(processed_data[0].keys())
        else:
            fieldnames = ["First Name", "Last Name", "Email", "Email Valid?"]
        
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for contact in processed_data:
            writer.writerow(contact)
    
    # -------------------------------------------------------------------
    # 5. DISPLAY COMPLETION MESSAGE AND SAMPLE OUTPUT
    # -------------------------------------------------------------------
    print(f"\nProcessing complete! Results saved to '{output_file_path}'.\n")
    print("Sample output (first 5 rows):")
    for i, item in enumerate(processed_data[:5]):
        print(item)

# -----------------------------------------------------------------------
# ENTRY POINT
# -----------------------------------------------------------------------
if __name__ == "__main__":
    process_event_list()
