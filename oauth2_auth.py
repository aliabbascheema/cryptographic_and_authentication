from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
authorization_base_url = os.getenv('AUTHORIZATION_URL')
token_url = os.getenv('TOKEN_URL')
redirect_uri = os.getenv('REDIRECT_URL')

# Function to automate OAuth flow


def get_access_token():
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri)
    authorization_url, state = oauth.authorization_url(authorization_base_url)
    print(f"Go to: {authorization_url}")
    redirect_response = input("Paste the full redirect URL after approval: ")
    token = oauth.fetch_token(
        token_url, authorization_response=redirect_response, client_secret=client_secret
    )
    return token

# Testing get user details using OAuth2 session token generated
def fetch_protected_resource(token):
    oauth = OAuth2Session(client_id, token=token)
    response = oauth.get("https://api.github.com/user")
    return response.json()

user_info = fetch_protected_resource(get_access_token())
print(f"User Info: {user_info}")
