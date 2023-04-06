import webbrowser
import requests
import os
import pandas as pd
from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
from quickbooks import QuickBooks
from quickbooks.objects.journalentry import JournalEntry

# Set up OAuth2 credentials
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = os.getenv('REDIRECT_URI')
environment = 'sandbox'  # set to 'production' for production environment
auth_client = AuthClient(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    environment=environment
)

# Generate authorization URL and open browser for user to authenticate
auth_url = auth_client.get_authorization_url([Scopes.ACCOUNTING])
webbrowser.open(auth_url)

# Automatically fetch the access token and realm ID after the user logs in
auth_header = None
while auth_header is None:
    # Check if the access token and realm ID are available
    if auth_client.access_token and auth_client.realm_id:
        auth_header = {'Authorization': f'Bearer {auth_client.access_token}'}
        client = QuickBooks(
            auth_client=auth_client,
            refresh_token=os.getenv('REFRESH_TOKEN'),
            company_id=os.getenv('COMPANY_ID')
        )
        print("User successfully authenticated.")
    else:
        # Wait for the user to log in and redirect to the callback URL
        try:
            response = requests.get(auth_url)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"Error: {e}")
            break
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            break
        else:
            continue

if auth_header is not None:
    # Get all journal entries
    journal_entry = JournalEntry()
    journal_entries = journal_entry.all(qb=client)

    # Create a pandas DataFrame from the journal entries
    data = []
    for entry in journal_entries:
        data.append(entry.to_dict())
    df = pd.DataFrame(data)
    print(df)
else:
    print("Unable to authenticate the user.")
