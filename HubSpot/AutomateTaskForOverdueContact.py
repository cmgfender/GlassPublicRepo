from hubspot import HubSpot
from datetime import datetime, timedelta

# HubSpot API client
api_client = HubSpot(api_key='your_hubspot_api_key')

# Calculate overdue date
overdue_date = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')

# Query contacts with last contact date older than overdue date
all_contacts = []
has_more = True
after = None

while has_more:
    response = api_client.crm.contacts.basic_api.get_page(limit=100, after=after, properties=['email', 'lastmodifieddate'])
    contacts = response.results
    all_contacts.extend(contacts)
    after = response.paging.next.after if response.paging else None
    has_more = after is not None

overdue_contacts = [
    contact for contact in all_contacts
    if contact.properties.get('lastmodifieddate') and contact.properties['lastmodifieddate'][:10] < overdue_date
]

# Create tasks for overdue contacts
for contact in overdue_contacts:
    task = {
        "engagement": {"type": "TASK"},
        "associations": {"contactIds": [contact.id]},
        "metadata": {
            "subject": f"Follow up with {contact.properties.get('email', 'Unknown')}",
            "status": "NOT_STARTED",
            "priority": "HIGH"
        }
    }
    api_client.crm.engagements.basic_api.create(task)
    print(f"Task created for overdue contact: {contact.properties.get('email', 'Unknown')}")

print("Task creation completed.")