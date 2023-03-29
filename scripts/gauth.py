from google_auth_oauthlib.flow import Flow
import json

# Set the scope - can be a list of scope strings
scope = 'https://www.googleapis.com/auth/spreadsheets'
# Load the client secrets file
with open(client_secrets_file, "r") as read_file:
    client_secrets_dict = json.load(read_file)
# Initialize flow object
flow = Flow.from_client_secrets_file(
    client_secrets_file='client_secrets_filename',
    scopes=scope,
    redirect_uri=client_secrets_dict['installed']['redirect_uris']
)

# Get authorization url
auth_url, _ = flow.authorization_url(prompt='consent')
print('Please go to this URL: {}'.format(auth_url))
# Input authorization code
code = input('Enter the authorization code:')
token = flow.fetch_token(code=code)
# Obtain authorized session
session = flow.authorized_session()