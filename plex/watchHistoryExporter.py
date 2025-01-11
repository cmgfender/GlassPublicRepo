"""
===========================================================
Script: Plex Server Watch History Exporter
===========================================================
Purpose:
--------
This script connects to a Plex Media Server to extract the watch history of all users. 
The watch history is then saved to a JSON file for further analysis or archival purposes.

Key Features:
-------------
1. Configurable Plex server URL and authentication token.
2. Retrieves watch history for all users linked to the Plex account.
3. Saves the watch history in a structured JSON file.
4. Provides detailed feedback during execution.
5. Handles errors such as invalid server URLs or tokens.

Usage:
------
1. Replace `PLEX_URL` and `PLEX_TOKEN` with your Plex server URL and token.
2. Run the script to generate a JSON file containing the watch history.
3. Open the JSON file to view the extracted data.

Dependencies:
-------------
- Python 3.x
- plexapi library (install via `pip install plexapi`)

===========================================================
"""

# Import necessary libraries
import json  # For saving the watch history as a JSON file
from plexapi.server import PlexServer  # For connecting to the Plex server

# ===========================
# Configuration Section
# ===========================

# Plex server URL and token: Replace these with your actual Plex server details
PLEX_URL = 'http://your_plex_server:32400'  # URL of your Plex server
PLEX_TOKEN = 'your_plex_token'  # Your Plex token for authentication

# Output file for saving watch history
output_file = 'watch_history.json'

# ===========================
# Step 1: Connect to Plex Server
# ===========================

try:
    print(f"Connecting to Plex server at {PLEX_URL}...")
    # Initialize a connection to the Plex server
    plex = PlexServer(PLEX_URL, PLEX_TOKEN)
    print("Connection to Plex server successful!")
except Exception as e:
    print(f"Error: Unable to connect to Plex server. Details: {e}")
    exit(1)  # Exit the script if the connection fails

# ===========================
# Step 2: Retrieve User Information
# ===========================

try:
    print("Retrieving user information...")
    # Get a list of all users associated with the Plex account
    users = plex.myPlexAccount().users()
    print(f"Found {len(users)} user(s).")
except Exception as e:
    print(f"Error: Unable to retrieve users. Details: {e}")
    exit(1)  # Exit if user retrieval fails

# ===========================
# Step 3: Collect Watch History
# ===========================

watch_history = {}  # Dictionary to store watch history for each user

try:
    print("Collecting watch history for each user...")
    for user in users:
        user_history = []  # List to store a user's watch history
        print(f"Processing watch history for user: {user.title}...")
        try:
            # Retrieve watch history for the user
            for item in plex.library.history(accountID=user.id):
                user_history.append({
                    'Title': item.title,  # Title of the watched item
                    'Watched At': item.viewedAt  # Date and time when the item was watched
                })
            # Add the user's watch history to the main dictionary
            watch_history[user.title] = user_history
        except Exception as e:
            print(f"Warning: Could not retrieve history for user {user.title}. Details: {e}")
except Exception as e:
    print(f"Error: Unable to collect watch history. Details: {e}")
    exit(1)  # Exit if watch history collection fails

# ===========================
# Step 4: Save Watch History to JSON
# ===========================

try:
    print(f"Saving watch history to {output_file}...")
    # Save the watch history to a JSON file
    with open(output_file, 'w') as f:
        json.dump(watch_history, f, indent=4)
    print(f"Watch history successfully saved to '{output_file}'!")
except Exception as e:
    print(f"Error: Unable to save watch history to file. Details: {e}")
    exit(1)  # Exit if saving the file fails

# ===========================
# Summary of Execution
# ===========================

print("\n--- Process Summary ---")
print(f"Plex Server: {PLEX_URL}")
print(f"Output File: {output_file}")
print("Script execution completed successfully!")

# ===========================
# Additional Notes
# ===========================
# - Ensure that the Plex server URL and token are valid.
# - The output JSON file contains watch history organized by user.
# - Extend the script to filter watch history by date or media type if needed.
