from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
from quickbooks import QuickBooks
from quickbooks.objects.journalentry import JournalEntry, JournalEntryLine, JournalEntryLineDetail
from quickbooks.objects.base import Ref
from quickbooks.objects.account import Account
import requests
import pandas as pd 
import os

url = f'https://docs.google.com/spreadsheets/d/1OCdBUrNH4eSH5PUKa2UCocEVtcYT3EqXxL-GY8s3RL8/gviz/tq?tqx=out:csv&sheet=QBsheet'
df_upload = pd.read_csv(url, on_bad_lines='skip')


url = f'https://docs.google.com/spreadsheets/d/1aAIvASexMT5qHFtSWFHsFMGYOM5AEFnfxSQKkhBDn_U/gviz/tq?tqx=out:csv&sheet=TryReference'
df_reference = pd.read_csv(url, on_bad_lines='skip')

# print(df_reference.head(2))

# print(df_upload.head(2))


for entry in range(0,len(df_upload)):
    reference_no = df_upload['reference_no'].iloc[entry]
    print(reference_no)
    
    print(df_reference.loc[df_reference['Account'] == reference_no]['Glcode'].item())