from intuitlib.client import AuthClient
from quickbooks import QuickBooks
from quickbooks.objects.journalentry import JournalEntry, JournalEntryLine, JournalEntryLineDetail
from quickbooks.objects.base import Ref
import requests
import os

from dotenv import load_dotenv

auth_client = AuthClient(
        client_id='AB4XiqeiADPn6wsAicYbm8RNfKpFadd3ddHq81Ymyr8hwk36W0',
        client_secret='rQYGZucC4u5aSV0XZdESahxClde28wnHsptLlUxN',
        access_token='eyJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwiYWxnIjoiZGlyIn0..As14H_Hckep19t9Vp5gFRg.fbN7YVB9HOGyq9Wfe04bNXyO2wlwycTs-WWTF4MvyRHCE2R4nA_2d96ya4lqdnZt46L29XKGY4VPLDMz3DMDVDX2W-fwyWmJ6cDoRO1eDjk46VSHkx0xqBwoMuMp1S6Tg03ZtxbsOwmDZ_4e_1j8P9p3sMIq3f9TOwR6gPezRPzqRIJgcMCLdiX8tGYwOoT5YpK8rw8PFhthu7uQqpfLXa8Q4mecS-Wilehj6S_ynEPyylG3XOLHKAtFBZ-rvrDBPgsfWKyaVtuaHJlveL7ZzPoBotaCC0ZuCUkkITysVi2Kzkkdat-PGSEV3WD7NnXCEvxFGpGTNio3pQndn3k_FTdrwWeYgYdcjZyWaAa1YbY3MsYfUDshexjd13XjeqkOaOrmqKhho1lnZtzeFUF3eaZl11Aj5ZKUm6B7uKvxPKyVKh7bDHzr7KIw1m8Yg9lml78sCuPPCgvnSWQ4DlMPZV5E3nsYTdvDybJOuyCenmjKtiahwiWvF03jgWJY5PTTUj7FGjC1KGX7JLKIl9mTdL7cKZ1wHfW8k0DCqnsvYADbUAZpONOR4n2q_I7vaTE06Su-PJQqdpQZRzYdOFdmqSzJyb8xyo00gGlPCwh2rIazDrmEi1l7BCLO9DiFJvUm2yNxGm2-cqvRxDOJEXvKFC8VwlOEDqmkXd1X-yGwZ0zTvLXIw8bsAKc28od8LcKUchIql6BUMaZ8AkDHMWohGUScxQ1PxVxNySRkTbTP1hRdftIV_Vkt4wyef7_ykfawCwDw1E_OHsFYgZCbXLN2ang5_G-HJCDsd7i3_enwPL026Uy4fXN9TJXVVRyzyYzeCk9CMGic1P3e_G_g4lIFcbdxftihtcodhliTf0ihmv-PJPucyf9npSwdMn662iNQD2laY2dVxE0vw9ermp61tw.gXZ5Bn7M_bZgKl_NMyGsWQ',
        environment='sandbox',
        redirect_uri='http://localhost:8000/callback',
    )

client = QuickBooks(
        auth_client=auth_client,
        refresh_token='AB11685799922xSy6apj44mzj1N8SY0d5Eil9xDH1FQHCu1gCI',
        company_id='4620816365281987550',
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

