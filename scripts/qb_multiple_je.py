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

#decalre a list of journal entries

journal_entry = JournalEntry()
journal_entry.Line = []
# validation for groupby and sum for account balance, calculate diff and should be zero.
# sort values +ve and -ve, then iterate through debits, credits


for entry in range(0,len(df_upload)):
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

    

    # journal_entry = JournalEntry()

    # journal_entry.Line = [line_one, line_two]
    # #append lines in the for loops in the list 

    # journal_entry.save(qb=client)


# for index, row in df_upload.iterrows():




#     #detail two 
#     detail_two = JournalEntryLineDetail()

#     detail_two.PostingType = df_upload['PostingType'].iloc[index+1] #journal_input["Line"][0]['JournalEntryLine1']['JournalEntryLineDetail']['PostingType']
#     detail_two.AccountRef = account_ref

#     line_two = JournalEntryLine()

#     line_two.JournalEntryLineDetail = detail_two
#     line_two.LineNum = 1
#     line_two.Description = df_upload['Description'].iloc[index+1]

#     amount = df_upload['Balance'].iloc[index+1]

#     line_two.Amount = amount.astype(str)

#     line_two.DetailType = "JournalEntryLineDetail"

#     journal_entry = JournalEntry()
#     journal_entry.Line = [line_one, line_two]
#     #append lines in the for loops in the list 

#     journal_entry.save(qb=client)




print("Task Finished")