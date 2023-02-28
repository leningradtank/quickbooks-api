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

journal_entry = JournalEntry()
journal_entry.Line = []

account_ref= Ref()

for entry in range(0,len(df_upload)):
    #get a specific account with a query 
    search_ref = df_upload['reference_no'].iloc[entry]
    print(search_ref)

    accounts = Account.where("id = '{}'".format(search_ref), qb=client)
    account_ref.value = search_ref

    account_ref.name = df_upload['reference_no'].iloc[entry]
    account_ref.type = df_upload['Type'].iloc[entry]

    detail_one = JournalEntryLineDetail()
    detail_one.PostingType = df_upload['PostingType'].iloc[entry]
    detail_one.AccountRef = account_ref

    line_one = JournalEntryLine()
    
    line_one.JournalEntryLineDetail = detail_one
    line_one.LineNum = 0
    line_one.Description = "ledgie activity for " + df_upload['system_date'].iloc[entry]

    amount = df_upload['balance'].iloc[entry]

    line_one.Amount = amount.astype(str)

    line_one.DetailType = "JournalEntryLineDetail"

    journal_entry.Line.append(line_one)

journal_entry.save(qb=client)