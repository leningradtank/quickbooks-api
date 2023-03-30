from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
from quickbooks import QuickBooks
from quickbooks.objects.journalentry import JournalEntry, JournalEntryLine, JournalEntryLineDetail
from quickbooks.objects.base import Ref
from quickbooks.objects.account import Account
import requests
import pandas as pd 
import os

from dotenv import load_dotenv
load_dotenv()

sheet_id = os.getenv('SHEET_ID')
sheet_name = os.getenv('SHEET_NAME')    

def auth():
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
    
    return client

def read_ledgie_data():
    #to be changed and instead read from ledgie db 
    df_ledgie = pd.read_csv('QBsheet.csv', on_bad_lines='skip')

    return df_ledgie


def read_from_google_sheet(sheet_id = sheet_id, sheet_name = sheet_name):
    url= f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    df_reference = pd.read_csv(url, on_bad_lines='skip')

    return df_reference



def upload():

    #read reference no for accounts
    df_upload = read_from_google_sheet(sheet_id = sheet_id, sheet_name = sheet_name)

    #read ledgie data 
    df_reference = read_ledgie_data()

    journal_entry = JournalEntry() #declare journal entry object
    journal_entry.Line = [] #empty list that will contain the journal entries for the day 

     #declare account reference object
    account_ref= Ref()

    for entry in range(0,len(df_upload)):

        #reference ledgie data account number with reference no from a google sheet
        
        reference_no = df_upload['reference_no'].iloc[entry]
        # print(reference_no)
        search_ref = df_reference.loc[df_reference['Account'] == reference_no]['Glcode'].item()
        

        #Cross referencing the reference number with account number and posting journal entry
        accounts = Account.where("id = '{}'".format(search_ref), qb=auth())
        
        account_ref.value = search_ref

        #Journal Entries

        account_ref.name = df_upload['Account'].iloc[entry]
        account_ref.type = df_upload['Type'].iloc[entry]

        detail_one = JournalEntryLineDetail()
        detail_one.PostingType = df_upload['PostingType'].iloc[entry]
        detail_one.AccountRef = account_ref

        #Only 1 Journal Line per Day

        line_one = JournalEntryLine()
        line_one.JournalEntryLineDetail = detail_one
        line_one.LineNum = 0
        line_one.Description = "ledgie activity for " + df_upload['system_date'].iloc[entry]

        amount = df_upload['balance'].iloc[entry]

        line_one.Amount = amount.astype(str)
        line_one.DetailType = "JournalEntryLineDetail"

        journal_entry.Line.append(line_one)

    journal_entry.save(qb=auth())
    print("done")
    

upload()