from intuitlib.client import AuthClient
from quickbooks import QuickBooks
from quickbooks.objects.journalentry import JournalEntry, JournalEntryLine, JournalEntryLineDetail
from quickbooks.objects.base import Ref
from quickbooks.objects.account import Account
import requests
import pandas as pd 
import os

from dotenv import load_dotenv
load_dotenv()

auth_client = AuthClient(
        client_id= os.getenv('CLIENT_ID'),
        client_secret= os.getenv('CLIENT_SECRET'),
        access_token= os.getenv('ACCESS_TOKEN'),
        environment='sandbox',
        redirect_uri='http://localhost:8000/callback',
    )

client = QuickBooks(
        auth_client=auth_client,
        refresh_token=os.getenv('REFRESH_TOKEN'),
        company_id=os.getenv('COMPANY_ID'),
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

df = pd.DataFrame()

for entry in journal_entries:
        all = entry.to_json()
        df.append
        print(entry.to_json())

#get all accounts and details

# accounts = Account.all(qb=client)

# df = pd.DataFrame()

# for account in accounts:
#         all = account.to_json()
#         print(all)
#         # df = df.append(pd.read_json(all))
#         # # df.append
#         # df.to_csv('all_accounts.csv')
        
# print("done")