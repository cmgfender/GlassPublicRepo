"""
===========================================================
Script: Sync Plex Watch History with Trakt
===========================================================
Purpose:
--------
This script syncs the watch history from a Plex Media Server with a Trakt account. 
It retrieves the list of watched movies from Plex and updates the Trakt history accordingly.

Key Features:
-------------
1. Fetches watched history from a specified Plex library.
2. Searches for corresponding movies on Trakt and syncs the watch status.
3. Configurable Plex and Trakt credentials.
4. Provides detailed feedback for each synced movie.
5. Error handling for missing or unmatched movies.

Usage:
------
1. Replace `PLEX_URL`, `PLEX_TOKEN`, `TRAKT_CLIENT_ID`, `TRAKT_CLIENT_SECRET`, and 
   `TRAKT_ACCESS_TOKEN` with your credentials.
2. Ensure that the Plex library section name matches your setup.
3. Run the script to sync Plex watch history with Trakt.

Dependencies:
-------------
- Python 3.x
- plexapi library (install via `pip install plexapi`)
- trakt.py library (install via `pip install trakt.py`)

===========================================================
"""

# Import necessary libraries
from plexapi.server import PlexServer  # For connecting to the Plex server
from trakt import Trakt  # For interacting with the Trakt API
from trakt.movies import Movie  # For searching movies on Trakt
import datetime  # For handling date and time

# ===========================
# Configuration Section
# ===========================

# Plex server configuration: Replace with your actual Plex server details
PLEX_URL = 'http://your_plex_server:32400'  # URL of your Plex server
PLEX_TOKEN = 'your_plex_token'  # Plex token for authentication

# Trakt API configuration: Replace with your actual Trakt API credentials
TRAKT_CLIENT_ID = 'your_trakt_client_id'
TRAKT_CLIENT_SECRET = 'your_trakt_client_secret'
TRAKT_ACCESS_TOKEN = 'your_trakt_access_token'

# Plex library to fetch watched history from
library_name = 'Movies'  # Change this to the relevant section in your Plex server

# ===========================
# Step 1: Authenticate Trakt
# ===========================

try:
    print("Authenticating with Trakt...")
    # Set Trakt API credentials
    Trakt.configuration.defaults.client(TRAKT_CLIENT_ID, TRAKT_CLIENT_SECRET)
    Trakt.configuration.defaults.oauth(token=TRAKT_ACCESS_TOKEN)
    print("Trakt authentication successful!")
except Exception as e:
    print(f"Error: Unable to authenticate with Trakt. Details: {e}")
    exit(1)  # Exit if Trakt authentication fails

# ===========================
# Step 2: Connect to Plex Server
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
# Step 3: Fetch Watched Movies from Plex
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
# Step 4: Sync Watched History with Trakt
# ===========================

for video in watched_movies:
    try:
        # Extract movie details from Plex
        watched_date = video.lastViewedAt
        title = video.title
        year = video.year

        print(f"Syncing {title} ({year}) watched on {watched_date}...")

        # Search for the movie on Trakt
        movie = Movie.search(f"{title} ({year})").first()

        if movie:
            # Sync watch history with Trakt
            Trakt['sync/history'].add({
                'movies': [{
                    'ids': movie.ids,  # Trakt movie IDs
                    'watched_at': watched_date.isoformat()  # ISO format for the watch date
                }]
            })
            print(f"Successfully synced {title} ({year}) to Trakt.")
        else:
            print(f"Warning: Movie '{title} ({year})' not found on Trakt.")
    except Exception as e:
        print(f"Error: Failed to sync '{title} ({year})'. Details: {e}")

# ===========================
# Summary of Execution
# ===========================

print("\n--- Process Summary ---")
print(f"Plex Server: {PLEX_URL}")
print(f"Trakt Account: {TRAKT_CLIENT_ID}")
print(f"Library Name: {library_name}")
print("Script execution completed successfully!")

# ===========================
# Additional Notes
# ===========================
# - Ensure that Plex and Trakt credentials are valid.
# - The script only syncs watched movies. Extend it to handle TV shows if needed.
# - Use Trakt API documentation for advanced features like removing watch history.