import os
import google.auth.transport.requests
import google_auth_oauthlib.flow
import googleapiclient.discovery
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
CLIENT_SECRETS_FILE = "client_secret.json"
TOKEN_NAME = "token.json"

def getAuthService():
    creds = None
    if os.path.exists(TOKEN_NAME):
        creds = Credentials.from_authorized_user_file(TOKEN_NAME, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google.auth.transport.requests.Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_console()
        with open(TOKEN_NAME, 'w') as token:
            token.write(creds.to_json())
    return googleapiclient.discovery.build("youtube", "v3", credentials=creds)

if __name__ == "__main__":
    service = getAuthService()
    print("Authentication successful, token.json created.")
