import webbrowser
from intuitlib.client import AuthClient
from intuitlib.enums import Scopes

# Set up OAuth2 credentials
client_id = 'your_client_id_here'
client_secret = 'your_client_secret_here'
redirect_uri = 'your_redirect_uri_here'
environment = 'sandbox'  # set to 'production' for production environment
auth_client = AuthClient(client_id, client_secret, redirect_uri, environment)

# Generate authorization URL and open browser for user to authenticate
auth_url = auth_client.get_authorization_url([Scopes.ACCOUNTING])
webbrowser.open(auth_url)

# Automatically fetch the access token and realm ID after the user logs in
auth_header = None
while auth_header is None:
    # Check if the access token and realm ID are available
    if auth_client.access_token and auth_client.realm_id:
        bearer_token = auth_client.access_token
        realm_id = auth_client.realm_id
        auth_header = f'Bearer {bearer_token}'
    else:
        # Wait for the user to log in and redirect to the callback URL
        print("Unable to log in")

# Make API call using bearer token and realm ID
base_url = f'https://{environment}-quickbooks.api.intuit.com'
url = f'{base_url}/v3/company/{realm_id}/companyinfo/{realm_id}'
headers = {
    'Authorization': auth_header,
    'Accept': 'application/json'
}
response = requests.get(url, headers=headers)
print(response.json())
