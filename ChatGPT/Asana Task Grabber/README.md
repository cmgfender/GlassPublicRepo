
# Asana Task Query API

This project is a serverless AWS Lambda function designed to query tasks from a specific Asana project and return task details such as name, assignee, due date, and notes. The API is RESTful and can be integrated with other systems to manage marketing calendar tasks.

---

## Features

- Retrieve Asana tasks based on a specified project ID.
- Filter tasks by due date (exact date or partial month).
- Specify the maximum number of tasks to retrieve.
- JSON-formatted responses for seamless integration.

---

## Setup

### 1. Environment Variables

Set the following environment variables in your deployment environment (e.g., AWS Lambda, local `.env` file, etc.):

- `ASANA_PAT`: Your Asana Personal Access Token.
- `ASANA_WORKSPACE_GID`: The Global ID of your Asana workspace.
- `ASANA_PROJECT_GID`: The Global ID of the Asana project to query.

### 2. Deployment

Deploy the Lambda function using one of the following methods:
- **AWS CLI**
- **AWS Management Console**
- **CI/CD Pipeline (e.g., GitHub Actions, Jenkins)**

### 3. API Gateway

Configure an API Gateway to trigger the Lambda function. Use the included OpenAPI schema (`openapi.yaml`) for quick setup.

---

## Usage

### HTTP Method: `GET`

### Endpoint

The API Gateway URL where the Lambda function is deployed. Replace `<API_BASE_URL>` with your actual API URL.

```
<API_BASE_URL>/asana_marketingcal
```

### Query Parameters

- `project_id` (required): The ID of the Asana project to retrieve tasks from.
- `due_date` (optional): Filter tasks by due date. Accepts:
  - `YYYY-MM` for a specific month.
  - `YYYY-MM-DD` for a specific date.
- `limit` (optional): Maximum number of tasks to retrieve (default: 20).

### Example Request

```
GET <API_BASE_URL>/asana_marketingcal?project_id=1202651676885035&due_date=2024-06&limit=10
```

---

## Response

The API returns a JSON array of task objects with the following structure:

```json
[
  {
    "name": "Task 1",
    "assignee": "John Doe",
    "due_date": "2024-06-10",
    "notes": "Details about Task 1"
  },
  {
    "name": "Task 2",
    "assignee": null,
    "due_date": null,
    "notes": ""
  }
]
```

---

## Error Handling

Errors are returned in the following format:

```json
{
  "error": "Failed to search tasks: <error message>"
}
```

---

## OpenAPI Specification

An OpenAPI 3.1.0 specification is included in this project to simplify API integration and documentation. Update the `servers` section with your deployment URL.

---

## Development

### Prerequisites

- Python 3.8 or later
- AWS CLI (for deployment)
- `requests` library (install via `pip install requests`)

### Running Locally

1. Set up environment variables in a `.env` file.
2. Run the function locally using a test event:

```bash
python lambda_function.py
```

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.
