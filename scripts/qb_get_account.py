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

df_upload = pd.read_csv('qb_data_2.csv')

#get a specific account with a query 
search_ref = df_upload['reference_no'].iloc[1]
print(search_ref)
accounts = Account.where("id = '{}'".format(search_ref), qb=client)

for account in accounts:
        all = account.to_json()
        print(all)


# print(account.to_json())
print("done")