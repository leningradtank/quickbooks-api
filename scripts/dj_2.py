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
    # read reference no for accounts
    df_upload = read_from_google_sheet(sheet_id=sheet_id, sheet_name=sheet_name)

    # read ledgie data 
    df_reference = read_ledgie_data()

    # create a list of JournalEntryLine objects
    lines = []
    for index, row in df_upload.iterrows():
        reference_no = row["reference_no"]
        search_ref = df_reference.loc[df_reference['Account'] == reference_no]['Glcode'].item()
        account_ref = Ref(value=search_ref, name=row["Account"], type=row["Type"])
        detail_one = JournalEntryLineDetail(PostingType=row["PostingType"], AccountRef=account_ref)
        line_one = JournalEntryLine(JournalEntryLineDetail=detail_one, LineNum=0, Description="ledgie activity for " + row["system_date"],
                                    Amount=str(row["balance"]), DetailType="JournalEntryLineDetail")
        lines.append(line_one)

    # create a JournalEntry object and save it
    journal_entry = JournalEntry(Line=lines)
    journal_entry.save(qb=auth())
    print("done")

    

upload()