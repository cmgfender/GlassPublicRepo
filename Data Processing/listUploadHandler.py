import csv
import re
import os

def is_valid_email(email: str) -> bool:
    """
    Checks if an email address is valid using a simple regex.
    NOTE: In practice, you may want to implement more robust validation 
    or use a dedicated library, but this works for many cases.
    """
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return True if re.match(email_regex, email) else False

def split_name(full_name: str):
    """
    Splits a full name string into first name and last name. 
    For simple cases, we'll split by the first space we see.
    If there's only one word, we'll treat it as first name only.
    For more robust name splitting, you'd want a more sophisticated approach.
    """
    # Strip leading/trailing whitespace
    full_name = full_name.strip()
    
    # Handle empty or None values
    if not full_name:
        return ("", "")
    
    # Split on spaces
    parts = full_name.split()
    
    # If there's only one name (e.g., "Madonna"), treat it as first name
    if len(parts) == 1:
        return (parts[0], "")
    
    # Return the first word as first name, the rest as last name
    # e.g. "John James Smith" -> first="John", last="James Smith"
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
    Main logic to handle uploading, processing, and formatting event contact lists
    for a CRM system.
    """
    # -------------------------------------------------------------------
    # 1. Get input CSV file path from the user
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
    # 2. Read the CSV file
    # -------------------------------------------------------------------
    # We’ll store processed rows in a list of dictionaries.
    processed_data = []
    
    # Open the CSV file
    with open(input_file_path, "r", encoding="utf-8-sig") as infile:
        reader = csv.DictReader(infile)
        
        # Identify the columns that exist in the file
        # Example known columns: 'Full Name', 'First Name', 'Last Name', 'Email', etc.
        # (We will do basic detection and handle them accordingly.)
        
        # Some possible columns we want to handle:
        possible_name_columns = ["Name", "Full Name", "Participant Name"]
        possible_first_name_columns = ["First Name", "FName", "FirstName"]
        possible_last_name_columns = ["Last Name", "LName", "LastName"]
        possible_email_columns = ["Email", "E-mail", "Email Address"]
        
        # Attempt to detect name columns automatically
        detected_full_name_col = None
        detected_first_name_col = None
        detected_last_name_col = None
        detected_email_col = None
        
        # For each column name in the CSV, see if it matches any known pattern
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
            # Ask user for column if not found
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
        # 3. Process each row
        # -------------------------------------------------------------------
        for row in reader:
            # Attempt to fetch First Name and Last Name
            first_name = ""
            last_name = ""
            
            # If we have a dedicated first name column
            if detected_first_name_col and detected_first_name_col in row:
                first_name = row[detected_first_name_col].strip()
            
            # If we have a dedicated last name column
            if detected_last_name_col and detected_last_name_col in row:
                last_name = row[detected_last_name_col].strip()
            
            # If those columns are empty or not provided, but we have a full name column
            if (not first_name or not last_name) and detected_full_name_col and detected_full_name_col in row:
                name_string = row[detected_full_name_col]
                split_first, split_last = split_name(name_string)
                # Only override if we had no value in first/last name
                if not first_name:
                    first_name = split_first
                if not last_name:
                    last_name = split_last
            
            # Email
            email = ""
            if detected_email_col and detected_email_col in row:
                email = row[detected_email_col].strip()
            
            # Validate email, mark invalid if needed
            email_valid = is_valid_email(email) if email else False
            
            # Build a standardized dictionary to represent this contact
            processed_contact = {
                "First Name": first_name,
                "Last Name": last_name,
                "Email": email,
                "Email Valid?": "Yes" if email_valid else "No"
            }
            
            # You could also copy over other columns from your CSV if desired
            # For example, if there's a "Company" column:
            #   processed_contact["Company"] = row.get("Company", "").strip()
            
            processed_data.append(processed_contact)
    
    # -------------------------------------------------------------------
    # 4. Write the output to a new CSV (or optionally process it in memory)
    # -------------------------------------------------------------------
    output_file_path = get_user_input(
        prompt="Enter the desired output CSV file name/path", 
        default_value="processed_event_list.csv"
    )
    
    with open(output_file_path, "w", newline="", encoding="utf-8") as outfile:
        # Determine fieldnames from the keys of the first dictionary in processed_data
        if processed_data:
            fieldnames = list(processed_data[0].keys())
        else:
            # If there's no data, let's define a default set of columns
            fieldnames = ["First Name", "Last Name", "Email", "Email Valid?"]
        
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for contact in processed_data:
            writer.writerow(contact)
    
    print(f"\nProcessing complete! Results saved to '{output_file_path}'.\n")
    print("Sample output (first 5 rows):")
    for i, item in enumerate(processed_data[:5]):
        print(item)

if __name__ == "__main__":
    process_event_list()
