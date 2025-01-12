import requests
import pandas as pd
from sqlalchemy import create_engine
from concurrent.futures import ThreadPoolExecutor
import time
import logging
from retrying import retry

# Configuration section
# Set up your Confluence API base URL, authentication details, and database connection
BASE_URL = "https://your-confluence-instance.atlassian.net/wiki/rest/api"  # Confluence base URL
USERNAME = "your_email@example.com"  # Confluence username (usually your email)
API_TOKEN = "your_api_token"  # Confluence API token for authentication
DB_ENGINE = create_engine('postgresql://username:password@localhost:5432/confluence_db')  # PostgreSQL database connection

# Specify which Confluence spaces and content types to extract
CONFLUENCE_SPACES = ["SPACE1", "SPACE2"]  # Replace with your Confluence space keys
CONTENT_TYPES = ["page", "blogpost"]  # Content types to fetch: 'page' for regular pages, 'blogpost' for blogs

# Logging setup for better tracking and debugging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Retry mechanism to handle transient network or API failures
@retry(wait_exponential_multiplier=1000, stop_max_attempt_number=5)
def make_request(url, params):
    """
    Makes a GET request to the Confluence API with retry capabilities.
    Retries in case of network or server errors.
    """
    response = requests.get(url, auth=(USERNAME, API_TOKEN), params=params)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

# Fetch Confluence content based on space and content type
def fetch_content(space_key, content_type, start=0, limit=50):
    """
    Fetches content from Confluence using the API.
    Supports pagination via 'start' and 'limit'.
    """
    url = f"{BASE_URL}/content"
    params = {
        "spaceKey": space_key,  # Restrict content to a specific Confluence space
        "type": content_type,   # Specify content type: 'page' or 'blogpost'
        "start": start,         # Pagination start index
        "limit": limit,         # Maximum number of results to fetch per request
        "expand": "body.storage,version,space,metadata,children.attachment,children.comment,history.contributors"
    }
    return make_request(url, params)

# Retrieve all content for a specific space and content type
def fetch_all_content(space_key, content_type):
    """
    Fetches all content of a given type (e.g., 'page', 'blogpost') from a Confluence space.
    Handles pagination to retrieve large datasets.
    """
    start = 0
    limit = 50  # Number of records to fetch per API call
    all_data = []  # Store all fetched content here

    while True:
        logging.info(f"Fetching {content_type} from space {space_key}, start={start}")
        data = fetch_content(space_key, content_type, start, limit)
        results = data.get('results', [])  # Extract the actual content from the response

        if not results:  # Stop if there are no more results to fetch
            break

        # Process and normalize each content item
        for item in results:
            all_data.append({
                "id": item["id"],  # Unique content ID
                "type": content_type,
                "title": item["title"],  # Title of the page or blog
                "version": item["version"]["number"],  # Version number
                "space": space_key,  # Space to which this content belongs
                "content": item["body"]["storage"]["value"],  # Full content in storage format
                "attachments": [att["title"] for att in item.get("children", {}).get("attachment", {}).get("results", [])],  # List of attachment titles
                "comments": [comment["body"]["storage"]["value"] for comment in item.get("children", {}).get("comment", {}).get("results", [])],  # List of comment content
                "contributors": [user["username"] for user in item.get("history", {}).get("contributors", {}).get("users", [])],  # List of contributors
                "metadata": item.get("metadata", {})  # Additional metadata
            })

        # Move to the next batch of results
        start += limit
        time.sleep(0.5)  # Pause between requests to avoid hitting API rate limits

    return all_data

# Fetch all users from Confluence
def fetch_users():
    """
    Fetches all users from Confluence for auditing and attribution.
    """
    url = f"{BASE_URL}/user"
    params = {"limit": 100}  # Adjust limit if needed
    data = make_request(url, params)
    return [{"username": user["username"], "display_name": user["displayName"]} for user in data["results"]]

# Save extracted data to a database
def save_to_database(data, table_name):
    """
    Saves data to a specified database table.
    If the table exists, the data will be appended.
    """
    if data:
        df = pd.DataFrame(data)  # Convert data to a DataFrame for easier manipulation
        df.to_sql(table_name, DB_ENGINE, if_exists='append', index=False)  # Save data to database
        logging.info(f"Saved {len(data)} records to {table_name}.")
    else:
        logging.warning(f"No data to save for {table_name}.")

# Parallelized fetching and saving of data for each space
def process_space(space_key):
    """
    Fetches and processes all content types for a specific Confluence space.
    """
    for content_type in CONTENT_TYPES:
        data = fetch_all_content(space_key, content_type)
        save_to_database(data, f"confluence_{content_type}s")  # Save data to a corresponding table

# Main function to orchestrate the extraction process
def main():
    """
    Main entry point for the script.
    Fetches content from multiple spaces and saves it to a database.
    """
    logging.info("Starting data extraction...")

    # Process each space in parallel to speed up the extraction
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_space, space_key) for space_key in CONFLUENCE_SPACES]
        for future in futures:
            try:
                future.result()  # Ensure any errors are raised and logged
            except Exception as e:
                logging.error(f"Error processing space: {e}")

    # Fetch and save user data
    logging.info("Fetching and saving users...")
    users = fetch_users()
    save_to_database(users, "confluence_users")

    logging.info("Data extraction completed successfully.")

# Run the main function if this script is executed directly
if __name__ == "__main__":
    main()