from hubspot import HubSpot
from hubspot.crm.contacts import SimplePublicObjectInput

# HubSpot API client
api_client = HubSpot(api_key='your_hubspot_api_key')

# Sample data for upsert
contacts_data = [
    {'email': 'contact1@example.com', 'firstname': 'John', 'lastname': 'Doe', 'company': 'TechCorp'},
    {'email': 'contact2@example.com', 'firstname': 'Jane', 'lastname': 'Smith', 'company': 'FinServ'},
    {'email': 'contact3@example.com', 'firstname': 'Bob', 'lastname': 'Brown', 'company': 'HealthInc'}
]

# Bulk upsert
for contact in contacts_data:
    properties = {
        'email': contact['email'],
        'firstname': contact['firstname'],
        'lastname': contact['lastname'],
        'company': contact['company']
    }
    obj_input = SimplePublicObjectInput(properties=properties)
    api_client.crm.contacts.basic_api.create_or_update(contact['email'], obj_input)
    print(f"Upserted contact: {contact['email']}")

print("Bulk upsert completed.")