from intuitlib.client import AuthClient
from quickbooks import QuickBooks
from quickbooks.objects.journalentry import JournalEntry, JournalEntryLine, JournalEntryLineDetail
from quickbooks.objects.base import Ref
import requests
import os

from dotenv import load_dotenv

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



# journal_entry.from_json(
#  {
# "Line": [
#     {
#       "JournalEntryLineDetail": {
#         "PostingType": "Debit", 
#         "AccountRef": {
#           "name": "Opening Bal Equity", 
#           "value": "39"
#         }
#       }, 
#       "DetailType": "JournalEntryLineDetail", 
#       "Amount": 100.0, 
#       "Id": "0", 
#       "Description": "nov portion of rider insurance"
#     }, 
#     {
#       "JournalEntryLineDetail": {
#         "PostingType": "Credit", 
#         "AccountRef": {
#           "name": "Notes Payable", 
#           "value": "44"
#         }
#       }, 
#       "DetailType": "JournalEntryLineDetail", 
#       "Amount": 100.0, 
#       "Description": "nov portion of rider insurance"
#     }
#   ]
#  }
# )

account_ref= Ref()
account_ref.value = 5
account_ref.name = 'Fees Billed'
account_ref.type = 'Account'

detail_one = JournalEntryLineDetail()

detail_one.PostingType = "Debit" #journal_input["Line"][0]['JournalEntryLine1']['JournalEntryLineDetail']['PostingType']
detail_one.AccountRef = account_ref

line_one = JournalEntryLine()
journal_entry = JournalEntry()


line_one.JournalEntryLineDetail = detail_one
line_one.LineNum = 0
line_one.Description = "Hello"
line_one.Amount = 1003

line_one.DetailType = "JournalEntryLineDetail"

#------

detail_two = JournalEntryLineDetail()

detail_two.PostingType = "Credit" #journal_input["Line"][0]['JournalEntryLine1']['JournalEntryLineDetail']['PostingType']
detail_two.AccountRef = account_ref
line_two = JournalEntryLine()

line_two.JournalEntryLineDetail = detail_two
line_two.LineNum = 1
line_two.Description = "Hello"
line_two.Amount = 1003

line_two.DetailType = "JournalEntryLineDetail"

journal_entry = JournalEntry()
journal_entry.Line = [line_one, line_two]

journal_entry.save(qb=client)

print(journal_entry.Line)


def journalentry():
    #take parameters for details of each entry. Return JE object. including which account 

#factories in python
for account in df['account']:
    journal_entry.account = 

