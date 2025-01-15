"""
Google Analytics Reporting
--------------------------
This script uses the Google Analytics Reporting API (v4) to fetch analytics data
for a particular view (property). It then stores the data in a CSV file for later analysis.

Dependencies:
    pip install google-api-python-client oauth2client pandas

Setup:
    1. Create a service account in Google Cloud and download the JSON key.
    2. Enable the Analytics API in your Google Cloud project.
    3. Give the service account access to the Google Analytics property view you want to query.
    4. Replace SERVICE_ACCOUNT_FILE with the path to your JSON key.
    5. Replace VIEW_ID with the numeric View (Profile) ID in your GA account.

Usage:
    1. Run the script. It will use the service account credentials to fetch data.
    2. The results are stored in a CSV file for analysis.
"""

import os
import pandas as pd
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import datetime

# Path to service account JSON key
SERVICE_ACCOUNT_FILE = "path/to/your-service-account.json"

# Google Analytics View (Profile) ID
VIEW_ID = "123456789"

def initialize_analyticsreporting():
    """
    Initializes the analyticsreporting service object using service account credentials.
    
    Returns:
        googleapiclient.discovery.Resource: The analyticsreporting resource.
    """
    # Define the scopes needed
    scopes = ["https://www.googleapis.com/auth/analytics.readonly"]

    # Authenticate and construct service
    credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, scopes)
    analytics = build("analyticsreporting", "v4", credentials=credentials)
    return analytics

def get_report(analytics, start_date="2023-01-01", end_date="2023-01-31"):
    """
    Queries the Analytics Reporting API V4.

    Args:
        analytics (Resource): The initialized analyticsreporting resource.
        start_date (str): Start date for the data to be fetched (YYYY-MM-DD).
        end_date (str): End date for the data to be fetched (YYYY-MM-DD).

    Returns:
        dict: The response from the Analytics Reporting API.
    """
    return analytics.reports().batchGet(
        body={
            "reportRequests": [
                {
                    "viewId": VIEW_ID,
                    "dateRanges": [{"startDate": start_date, "endDate": end_date}],
                    "metrics": [{"expression": "ga:users"}, {"expression": "ga:sessions"}, {"expression": "ga:pageviews"}],
                    "dimensions": [{"name": "ga:date"}],
                }
            ]
        }
    ).execute()

def parse_response(response):
    """
    Parses the API response and returns data in a list of dictionaries format.
    
    Args:
        response (dict): The response from the Analytics Reporting API.

    Returns:
        list: A list of dictionaries containing date, users, sessions, pageviews.
    """
    reports = response.get("reports", [])
    data_list = []

    for report in reports:
        rows = report.get("data", {}).get("rows", [])
        for row in rows:
            date = row["dimensions"][0]  # 'ga:date'
            metrics = row["metrics"][0]["values"]  # [users, sessions, pageviews]
            data_dict = {
                "Date": date,
                "Users": metrics[0],
                "Sessions": metrics[1],
                "Pageviews": metrics[2],
            }
            data_list.append(data_dict)
    return data_list

def store_data_to_csv(data, filename="analytics_data.csv"):
    """
    Stores the retrieved analytics data into a CSV file.

    Args:
        data (list): A list of dictionaries.
        filename (str): The name of the CSV file to store data.
    """
    if not data:
        print("No analytics data to store.")
        return

    df = pd.DataFrame(data)

    # Convert date from 'YYYYMMDD' to a proper date format
    df["Date"] = pd.to_datetime(df["Date"], format="%Y%m%d")

    # Save to CSV
    df.to_csv(filename, index=False)
    print(f"Saved analytics data to {filename}")

def main():
    analytics = initialize_analyticsreporting()
    response = get_report(analytics, start_date="2023-01-01", end_date="2023-01-31")
    data = parse_response(response)
    store_data_to_csv(data)

if __name__ == "__main__":
    main()
