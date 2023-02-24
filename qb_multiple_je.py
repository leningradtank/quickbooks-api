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

account_ref= Ref()
account_ref.value = 114


# validation for groupby and sum for account balance, calculate diff and should be zero.
# sort values +ve and -ve, then iterate through debits, credits

for index, row in df_upload.iterrows():
    account_ref.name = df_upload['Account'].iloc[index]
    account_ref.type = df_upload['Type'].iloc[index]

    detail_one = JournalEntryLineDetail()
    detail_one.PostingType = df_upload['PostingType'].iloc[index]
    detail_one.AccountRef = account_ref

    line_one = JournalEntryLine()
    journal_entry = JournalEntry()

    line_one.JournalEntryLineDetail = detail_one
    line_one.LineNum = 0
    line_one.Description = df_upload['Description'].iloc[index]

    amount = df_upload['Balance'].iloc[index]

    line_one.Amount = amount.astype(str)

    line_one.DetailType = "JournalEntryLineDetail"

    #detail two 
    detail_two = JournalEntryLineDetail()

    detail_two.PostingType = df_upload['PostingType'].iloc[index+1] #journal_input["Line"][0]['JournalEntryLine1']['JournalEntryLineDetail']['PostingType']
    detail_two.AccountRef = account_ref

    line_two = JournalEntryLine()

    line_two.JournalEntryLineDetail = detail_two
    line_two.LineNum = 1
    line_two.Description = df_upload['Description'].iloc[index+1]

    amount = df_upload['Balance'].iloc[index+1]

    line_two.Amount = amount.astype(str)

    line_two.DetailType = "JournalEntryLineDetail"

    journal_entry = JournalEntry()
    journal_entry.Line = [line_one, line_two]

    journal_entry.save(qb=client)




print("Task Finished")