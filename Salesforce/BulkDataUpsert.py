from simple_salesforce import Salesforce, SalesforceBulk
import pandas as pd
import csv

# Salesforce connection
sf = Salesforce(username='your_username', password='your_password', security_token='your_token')
bulk = SalesforceBulk(sf)

# Sample data to upsert
data = [
    {'External_Id__c': '1001', 'Name': 'Account 1', 'Industry': 'Technology'},
    {'External_Id__c': '1002', 'Name': 'Account 2', 'Industry': 'Finance'},
    {'External_Id__c': '1003', 'Name': 'Account 3', 'Industry': 'Healthcare'}
]

# Write data to CSV
csv_file = 'upsert_data.csv'
with open(csv_file, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)

# Bulk upsert
job = bulk.create_upsert_job("Account", external_id_field="External_Id__c", contentType='CSV')
with open(csv_file, 'rb') as f:
    bulk.post_batch(job, f)
bulk.close_job(job)

print("Bulk upsert completed.")