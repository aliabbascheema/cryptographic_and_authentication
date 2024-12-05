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
    """
    Retrieve an access token using the OAuth2 authorization flow. This function guides the user through the process of obtaining an access token by directing them to the authorization URL and handling the redirect response.

    It initializes an OAuth2 session, prompts the user to visit the authorization URL, and then fetches the access token using the provided redirect response. The function assumes that necessary OAuth2 parameters such as client_id, redirect_uri, and client_secret are defined in the surrounding context.

    Args:
        None

    Returns:
        dict: The access token information returned by the OAuth2 provider.

    Raises:
        ValueError: If the authorization response is invalid or the token cannot be fetched.
    """
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri)
    authorization_url, state = oauth.authorization_url(authorization_base_url)
    print(f"Go to: {authorization_url}")
    redirect_response = input("Paste the full redirect URL after approval: ")
    token = oauth.fetch_token(
        token_url, authorization_response=redirect_response, client_secret=client_secret
    )
    return token

# returning the generated token for testing purposes
token = get_access_token()
print(f"Access Token: {token}")

# Testing get user details using OAuth2 session token generated
oauth_session = OAuth2Session(client_id, token=token)
response = oauth_session.get("https://api.github.com/user")
print(response.json())
