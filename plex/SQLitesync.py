"""
===========================================================
Script: Plex Library Sync with SQLite Database
===========================================================
Purpose:
--------
This script connects to a Plex Media Server and synchronizes its library data 
with a local SQLite database. It stores details about media items (e.g., title, year, 
duration, rating, genres, and added date) in a structured database for further analysis.

Key Features:
-------------
1. Configurable Plex server URL, token, and SQLite database file.
2. Automatically creates the required SQLite table if it doesn't exist.
3. Inserts new media items and updates existing ones.
4. Handles missing or optional data (e.g., genres, ratings).
5. Provides detailed feedback during each step of the process.
6. Error handling for connection issues and database operations.

Usage:
------
1. Replace `PLEX_URL` and `PLEX_TOKEN` with your Plex server URL and token.
2. Set the desired SQLite database file name.
3. Run the script to sync your Plex library with the SQLite database.

Dependencies:
-------------
- Python 3.x
- plexapi library (install via `pip install plexapi`)

===========================================================
"""

# Import necessary libraries
import sqlite3  # For interacting with the SQLite database
from plexapi.server import PlexServer  # For connecting to the Plex server

# ===========================
# Configuration Section
# ===========================

# Plex server configuration: Replace with your actual Plex server details
PLEX_URL = 'http://your_plex_server:32400'  # Plex server URL
PLEX_TOKEN = 'your_plex_token'  # Plex token for authentication

# SQLite database file: Change this to your preferred database file name
db_file = 'plex_library.db'

# Plex library to sync: Adjust this to match the section name in your Plex server
library_name = 'Movies'

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
    exit(1)  # Exit the script if the connection fails

# ===========================
# Step 2: Set Up SQLite Database
# ===========================

try:
    print(f"Connecting to SQLite database: {db_file}...")
    # Connect to the SQLite database (creates the file if it doesn't exist)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    print("Database connection established successfully!")

    # Create the media table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS media (
        id INTEGER PRIMARY KEY,
        title TEXT,
        year INTEGER,
        duration INTEGER,
        rating FLOAT,
        genres TEXT,
        added_at TEXT
    )
    ''')
    print("Table 'media' is ready for use.")
except sqlite3.Error as e:
    print(f"Error: Unable to set up the database. Details: {e}")
    exit(1)  # Exit if the database setup fails

# ===========================
# Step 3: Fetch Plex Library
# ===========================

try:
    print(f"Fetching library section: '{library_name}'...")
    # Access the specified library section in Plex
    library = plex.library.section(library_name)
    print(f"Library '{library_name}' fetched successfully!")
except Exception as e:
    print(f"Error: Unable to access library '{library_name}'. Details: {e}")
    exit(1)  # Exit if the library section is not found

# ===========================
# Step 4: Sync Data with SQLite
# ===========================

try:
    print("Syncing library data with the database...")
    # Loop through all items in the Plex library
    for item in library.all():
        # Format genres as a comma-separated string
        genres = ', '.join([genre.tag for genre in item.genres]) if item.genres else ''
        
        # Insert or update the media item in the database
        cursor.execute('''
        INSERT OR REPLACE INTO media (id, title, year, duration, rating, genres, added_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (item.ratingKey, item.title, item.year, item.duration, item.rating, genres, item.addedAt))
    
    # Commit changes to the database
    conn.commit()
    print("Library data synced successfully!")
except sqlite3.Error as e:
    print(f"Error: Unable to sync data with the database. Details: {e}")
    exit(1)  # Exit if data syncing fails

# ===========================
# Step 5: Close Database Connection
# ===========================

try:
    # Close the database connection
    conn.close()
    print("Database connection closed.")
except sqlite3.Error as e:
    print(f"Error: Unable to close the database connection. Details: {e}")

# ===========================
# Summary of Execution
# ===========================

print("\n--- Process Summary ---")
print(f"Plex Server: {PLEX_URL}")
print(f"Library Name: {library_name}")
print(f"SQLite Database File: {db_file}")
print("Script execution completed successfully!")

# ===========================
# Additional Notes
# ===========================
# - Ensure the Plex server and library section names are correct.
# - The SQLite database file will be created in the same directory as the script unless a full path is provided.
# - Extend the script to handle additional libraries or add custom data fields.