from simple_salesforce import Salesforce
from datetime import datetime, timedelta

# Salesforce connection
sf = Salesforce(username='your_username', password='your_password', security_token='your_token')

# Calculate date range
today = datetime.today()
week_ahead = today + timedelta(days=7)
today_str = today.strftime('%Y-%m-%d')
week_ahead_str = week_ahead.strftime('%Y-%m-%d')

# Query opportunities
query = f"""
SELECT Id, Name, CloseDate
FROM Opportunity
WHERE CloseDate >= {today_str} AND CloseDate <= {week_ahead_str}
"""
opportunities = sf.query(query)['records']

# Create tasks
for opp in opportunities:
    task = {
        'Subject': f"Follow up on {opp['Name']}",
        'WhatId': opp['Id'],
        'ActivityDate': opp['CloseDate'],
        'Status': 'Not Started',
        'Priority': 'High'
    }
    sf.Task.create(task)
    print(f"Task created for Opportunity: {opp['Name']}")

print("Task creation completed.")