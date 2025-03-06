from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def authenticate_gmail():
    """Handles Gmail API authentication and token storage."""
    creds = None

    if os.path.exists("token.pkl"):
        with open("token.pkl", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists("credentials.json"):
                print("ERROR: credentials.json not found!")
                exit(1)
            print("Found credentials.json, proceeding with authentication...")

            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(host="localhost")

        with open("token.pkl", "wb") as token:
            pickle.dump(creds, token)

    return creds

def get_authenticated_user_email():
    """Fetches the email address of the currently authenticated user."""
    creds = authenticate_gmail()
    service = build("gmail", "v1", credentials=creds)
    
    profile = service.users().getProfile(userId="me").execute()
    return profile.get("emailAddress", "unknown_user@example.com")
