from intuitlib.client import AuthClient
from quickbooks import QuickBooks
from quickbooks.objects.journalentry import JournalEntry
import requests
import os

import pandas as pd 

from dotenv import load_dotenv
load_dotenv()

auth_client = AuthClient(
        client_id= os.getenv('client_id'),
        client_secret= os.getenv('client_secret'),
        access_token= os.getenv('access_token'),
        environment='sandbox',
        redirect_uri='http://localhost:8000/callback',
    )

client = QuickBooks(
        auth_client=auth_client,
        refresh_token=os.getenv('refresh_token'),
        company_id=os.getenv('company_id'),
    )

# from quickbooks.objects.customer import Customer
# customers = Customer.all(qb=client)

# customer = Customer()
# customer.CompanyName = "Test1"
# customer.FamilyName = "Alpaca2"
# customer.save(qb=client)

# value = Customer.filter(start_position=1, max_results=25, Active=True, CompanyName="Test1", qb=client)

# # print(value.CompanyName)

# # customers = Customer.filter(Active=True, FamilyName="Smith", qb=client)

# for customer in value:
#         print(customer.CompanyName)

journal_entry = JournalEntry()


journal_entries = journal_entry.all(qb=client)

for entry in journal_entries:
        print(entry.to_json())

