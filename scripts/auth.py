from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
import os

from dotenv import load_dotenv
load_dotenv()

client_id= os.getenv('client_id'),
client_secret= os.getenv('client_secret')
environment='sandbox'
redirect_uri='http://localhost:8000/callback'
company_id=os.getenv('company_id')

scopes = [
    Scopes.ACCOUNTING
]

auth_client = AuthClient(client_id, client_secret, redirect_uri, environment )
print(auth_client)
url = auth_client.get_authorization_url(scopes)

print(url)

# token = auth_client.get_bearer_token(auth_code, realm_id=realm_id)

