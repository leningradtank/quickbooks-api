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

def read_from_google_sheet(sheet_id = sheet_id, sheet_name = sheet_name):
    url= f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    df_reference = pd.read_csv(url, on_bad_lines='skip')

    

def auth():
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
    
    return client

def read_ledgie_data():
    #to be changed and instead read from ledgie db 
    df_ledgie = pd.read_csv('ledgie_data.csv')

    delta = df_ledgie['tot_net_amt'].sum()

    #check if the diff is 0 , as credits = debits
    if delta == 0:
        print('Delta is 0')
    else:
        print('Delta is not zero for this dataset')


url = f'https://docs.google.com/spreadsheets/d/1OCdBUrNH4eSH5PUKa2UCocEVtcYT3EqXxL-GY8s3RL8/gviz/tq?tqx=out:csv&sheet=QBsheet'
df_upload = pd.read_csv(url, on_bad_lines='skip')

def upload():

    #reference sheet for reference = account
    url = f'https://docs.google.com/spreadsheets/d/1aAIvASexMT5qHFtSWFHsFMGYOM5AEFnfxSQKkhBDn_U/gviz/tq?tqx=out:csv&sheet=TryReference'
    df_reference = pd.read_csv(url, on_bad_lines='skip')

    #read google csv data 


    journal_entry = JournalEntry() #declare journal entry object
    journal_entry.Line = [] #empty list that will contain the journal entries for the day 

     #declare account reference object
    account_ref= Ref()

    for entry in range(0,len(df_upload)):
        #get a specific account with a query 
        # search_ref = 114
        # df_upload['reference_no'].iloc[entry] 
        

        # accounts = Account.where("id = '{}'".format(search_ref), qb=auth())
        
        #adding what value of the account is from google sheets column
        # account_ref.value = search_ref
        print(df_upload['reference_no'].iloc[entry])
        account_ref.value = str(df_upload['reference_no'].iloc[entry])

        #next step will need to change dfupload to fetch(accounts.name and accounts.type) and convert from json to string

        account_ref.name = df_upload['Account'].iloc[entry]
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

    journal_entry.save(qb=auth())
    

upload()