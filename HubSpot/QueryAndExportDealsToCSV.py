from hubspot import HubSpot
import pandas as pd

# HubSpot API client
api_client = HubSpot(api_key='your_hubspot_api_key')

# Query deals
all_deals = []
has_more = True
after = None

while has_more:
    response = api_client.crm.deals.basic_api.get_page(limit=100, after=after, properties=['dealname', 'amount', 'dealstage'])
    deals = response.results
    all_deals.extend(deals)
    after = response.paging.next.after if response.paging else None
    has_more = after is not None

# Convert deals to DataFrame
deals_data = [
    {
        'ID': deal.id,
        'Name': deal.properties.get('dealname', 'N/A'),
        'Amount': deal.properties.get('amount', 'N/A'),
        'Stage': deal.properties.get('dealstage', 'N/A')
    }
    for deal in all_deals
]

df = pd.DataFrame(deals_data)

# Save to CSV
output_file = 'deals_export.csv'
df.to_csv(output_file, index=False)

print(f"Deals exported to {output_file}")