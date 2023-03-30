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

# df_upload = pd.read_csv('qb_data_2.csv')

#get a specific account with a query 
search_ref = 1
print(search_ref)
accounts = Account.where("id = '{}'".format(search_ref), qb=client)

for account in accounts:
        all = account.to_json()
        print(account.to_json())


# print(account.to_json())
print("done")