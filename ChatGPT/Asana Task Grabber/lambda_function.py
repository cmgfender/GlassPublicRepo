import os
import json
import requests
from datetime import datetime

def lambda_handler(event, context):
    # Asana Personal Access Token (PAT)
    asana_token = os.getenv("ASANA_PAT")  # Set as an environment variable
    workspace_gid = os.getenv("ASANA_WORKSPACE_GID")  # Environment variable for workspace GID
    project_gid = os.getenv("ASANA_PROJECT_GID")  # Environment variable for project GID
    headers = {"Authorization": f"Bearer {asana_token}"}
    
    # Retrieve query parameters
    params = event.get("queryStringParameters", {}) or {}
    due_date = params.get("due_date")  # e.g., "2024-06" or "2024-06-10"
    limit = int(params.get("limit", 20))
    
    # Construct search parameters
    search_params = {
        "projects.any": project_gid,
        "limit": limit,
        "opt_fields": "name,assignee.name,due_on,notes"
    }
    
    # Handle date filters
    if due_date:
        if len(due_date) == 10:  # Exact date
            search_params["due_on"] = due_date
        elif len(due_date) == 7:  # Partial date (YYYY-MM)
            search_params["due_after"] = f"{due_date}-01"
            year, month = map(int, due_date.split('-'))
            next_month = f"{year + (month // 12)}-{(month % 12) + 1:02d}-01"
            search_params["due_before"] = next_month

    search_url = f"https://app.asana.com/api/1.0/workspaces/{workspace_gid}/tasks/search"
    try:
        response = requests.get(search_url, headers=headers, params=search_params)
        response.raise_for_status()
        print("API Response:", json.dumps(response.json(), indent=2))  # Debug log
    except requests.exceptions.RequestException as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Failed to search tasks: {str(e)}"})
        }
    
    # Extract and format tasks
    tasks = response.json().get('data', [])
    filtered_tasks = [
        {
            "name": task.get("name"),
            "assignee": task.get("assignee", {}).get("name") if task.get("assignee") else None,
            "due_date": task.get("due_on"),
            "notes": task.get("notes"),
        }
        for task in tasks
    ]
    
    print(f"Filtered Tasks: {len(filtered_tasks)}")
    return {
        "statusCode": 200,
        "body": json.dumps(filtered_tasks)
    }