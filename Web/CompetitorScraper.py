"""
Competitor Website Scraper
--------------------------
This script scrapes competitor sites to gather product info, such as price, name,
and promotional details. It then stores the data in a CSV file for easy analysis.

Dependencies:
    pip install requests beautifulsoup4 pandas

Usage:
    1. Replace 'EXAMPLE_URL' with the actual competitor product page URL.
    2. Modify the parsing logic depending on the site's HTML structure.
    3. Run the script. Ensure you comply with website TOS and local laws.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

def fetch_product_data(url):
    """
    Fetches HTML content from the given URL and parses product information.
    
    Args:
        url (str): The competitor page URL to scrape.
        
    Returns:
        list of dict: A list containing product data dictionaries.
    """
    product_list = []

    # Send a GET request to the URL
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Example parse: find all product items by HTML tag/class
        # NOTE: Adjust selectors as needed for the competitor's site
        product_items = soup.find_all("div", class_="product-container")

        for item in product_items:
            try:
                product_name = item.find("h2", class_="product-name").text.strip()
                price = item.find("span", class_="price").text.strip()
                promotion = item.find("span", class_="promotion").text.strip() if item.find("span", class_="promotion") else ""

                product_data = {
                    "Product Name": product_name,
                    "Price": price,
                    "Promotion": promotion,
                    "Scraped At": datetime.datetime.now().isoformat()
                }

                product_list.append(product_data)
            except AttributeError:
                # In case any element is missing
                continue
    else:
        print(f"Failed to fetch {url} with status code {response.status_code}")

    return product_list

def store_data_to_csv(data, filename="competitor_data.csv"):
    """
    Append product data to a CSV file.
    
    Args:
        data (list): A list of dictionaries containing product data.
        filename (str): The CSV filename.
        
    Returns:
        None
    """
    if not data:
        print("No data to store.")
        return

    df = pd.DataFrame(data)

    try:
        existing_df = pd.read_csv(filename)
        combined_df = pd.concat([existing_df, df]).drop_duplicates()
    except FileNotFoundError:
        combined_df = df

    combined_df.to_csv(filename, index=False)
    print(f"{len(data)} new entries saved to {filename}.")

def main():
    # Example competitor product page URL
    competitor_url = "https://www.example.com/products"

    # Fetch product data from competitor site
    data = fetch_product_data(competitor_url)

    # Store or update CSV file with new data
    store_data_to_csv(data)

if __name__ == "__main__":
    main()
