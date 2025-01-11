"""
===========================================================
Script: Sync Plex Watch History with Letterboxd (Including Ratings)
===========================================================
Purpose:
--------
This script syncs the watch history from a Plex Media Server to a Letterboxd 
CSV file, including ratings. It fetches watched movies from Plex, formats the data 
(including title, year, watched date, and user ratings), and generates a CSV file 
compatible with Letterboxd.

Key Features:
-------------
1. Fetches watched history from a specified Plex library.
2. Includes ratings alongside movie titles, years, and watched dates.
3. Creates a properly structured CSV file for Letterboxd import.
4. Configurable Plex credentials, library name, and CSV output path.
5. Provides detailed feedback and error handling.

Usage:
------
1. Replace `PLEX_URL` and `PLEX_TOKEN` with your Plex server URL and token.
2. Set the desired Plex library and output CSV file name.
3. Run the script to generate a Letterboxd-compatible CSV file.
4. Follow the instructions below to import the CSV file into Letterboxd.

Letterboxd Import Instructions:
--------------------------------
1. Log in to your Letterboxd account.
2. Navigate to the **Import & Export** page: https://letterboxd.com/import/
3. In the "Import Your Data" section, upload the generated CSV file (`letterboxd_watch_history_with_ratings.csv`).
4. Choose the appropriate options for import:
   - Ensure the "Watched" checkbox is checked.
   - Optionally, choose to mark entries as "Liked" if desired.
5. Click **Upload** to start the import.
6. After the import is complete, verify your Letterboxd history to ensure all movies were added correctly.

Dependencies:
-------------
- Python 3.x
- pandas library (install via `pip install pandas`)
- plexapi library (install via `pip install plexapi`)

===========================================================
"""

# Import necessary libraries
from plexapi.server import PlexServer  # For connecting to the Plex server
import pandas as pd  # For creating and exporting the CSV file
import datetime  # For handling date and time

# ===========================
# Configuration Section
# ===========================

# Plex server configuration: Replace with your actual Plex server details
PLEX_URL = 'http://your_plex_server:32400'  # URL of your Plex server
PLEX_TOKEN = 'your_plex_token'  # Plex token for authentication

# Plex library to fetch watched history from
library_name = 'Movies'  # Change this to the relevant section in your Plex server

# Output CSV file for Letterboxd import
output_csv = 'letterboxd_watch_history_with_ratings.csv'

# ===========================
# Step 1: Connect to Plex Server
# ===========================

try:
    print(f"Connecting to Plex server at {PLEX_URL}...")
    # Initialize a connection to the Plex server
    plex = PlexServer(PLEX_URL, PLEX_TOKEN)
    print("Connected to Plex server successfully!")
except Exception as e:
    print(f"Error: Unable to connect to Plex server. Details: {e}")
    exit(1)  # Exit if the connection fails

# ===========================
# Step 2: Fetch Watched Movies from Plex
# ===========================

try:
    print(f"Fetching watched movies from Plex library: '{library_name}'...")
    library = plex.library.section(library_name)  # Access the specified Plex library
    watched_movies = library.search(watched=True)  # Get all watched movies
    print(f"Found {len(watched_movies)} watched movie(s) in Plex library.")
except Exception as e:
    print(f"Error: Unable to fetch movies from Plex library. Details: {e}")
    exit(1)  # Exit if the library or watched movies cannot be accessed

# ===========================
# Step 3: Prepare Data for Letterboxd (Including Ratings)
# ===========================

# Create a list to hold data for the CSV
csv_data = []

print("Preparing data for Letterboxd import...")
for video in watched_movies:
    try:
        # Extract movie details
        title = video.title
        year = video.year
        watched_date = video.lastViewedAt.strftime('%Y-%m-%d') if video.lastViewedAt else None
        rating = video.userRating if video.userRating is not None else ''  # Include user rating if available

        # Append data to the list in Letterboxd CSV format
        csv_data.append({
            'Title': title,  # Movie title
            'Year': year,  # Release year
            'Watched Date': watched_date,  # Date watched (formatted as YYYY-MM-DD)
            'Rating': rating  # User rating
        })
        print(f"Added: {title} ({year}), Watched on: {watched_date}, Rating: {rating}")
    except Exception as e:
        print(f"Warning: Failed to process movie '{title}' ({year}). Details: {e}")

# ===========================
# Step 4: Save Data to CSV
# ===========================

try:
    print(f"Saving watch history to CSV file: {output_csv}...")
    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(csv_data, columns=['Title', 'Year', 'Watched Date', 'Rating'])

    # Save the DataFrame as a CSV file
    df.to_csv(output_csv, index=False)
    print(f"Watch history successfully saved to '{output_csv}'!")
except Exception as e:
    print(f"Error: Unable to save watch history to CSV file. Details: {e}")
    exit(1)  # Exit if saving the CSV fails

# ===========================
# Summary of Execution
# ===========================

print("\n--- Process Summary ---")
print(f"Plex Server: {PLEX_URL}")
print(f"Library Name: {library_name}")
print(f"Output CSV File: {output_csv}")
print("Script execution completed successfully!")

# ===========================
# Additional Notes
# ===========================
# - Ensure that Plex credentials are valid.
# - The output CSV file can be imported into Letterboxd via the import tool.
# - Extend the script to include additional fields like genres or reviews if needed.