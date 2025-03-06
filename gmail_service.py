from googleapiclient.discovery import build
from gmail_auth import authenticate_gmail
from db import get_important_senders
from email_classifier import classify_email  # Use rule-based classifier
import base64
import re

def get_emails():
    """Fetches the latest unread emails from Gmail API."""
    creds = authenticate_gmail()
    service = build("gmail", "v1", credentials=creds)

    results = service.users().messages().list(userId="me", maxResults=10, q="is:unread").execute()
    messages = results.get("messages", [])

    emails = []
    for msg in messages:
        msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()
        headers = msg_data["payload"].get("headers", [])
        email_info = {
            "id": msg["id"],
            "from": next((h["value"] for h in headers if h["name"].lower() == "from"), "Unknown"),
            "subject": next((h["value"] for h in headers if h["name"].lower() == "subject"), "No Subject"),
            "snippet": msg_data.get("snippet", "No snippet available")
        }
        emails.append(email_info)
    
    return emails

def prioritize_emails(emails):
    """Assigns a priority score using both rule-based classifier and manual sender importance."""
    important_senders = get_important_senders()
    
    def calculate_priority(email):
        sender = email["from"].lower().strip()
        sender_score = 5 if sender in important_senders else 0
        ai_score = classify_email(email["snippet"])
        return sender_score + ai_score  # Max = 5 + 5 = 10
    
    for email in emails:
        email["priority"] = calculate_priority(email)
    
    return sorted(emails, key=lambda x: x["priority"], reverse=True)

def get_email_content(email_id):
    """Fetches the full content of an email given its ID."""
    creds = authenticate_gmail()
    service = build("gmail", "v1", credentials=creds)
    message = service.users().messages().get(userId="me", id=email_id, format="full").execute()
    payload = message.get("payload", {})
    headers = payload.get("headers", [])
    
    subject = next((h["value"] for h in headers if h["name"].lower() == "subject"), "No Subject")
    from_header = next((h["value"] for h in headers if h["name"].lower() == "from"), "Unknown Sender")
    sender_name = extract_sender_name(from_header)
    
    return {"id": email_id, "subject": subject, "sender": sender_name, "body": extract_email_body(payload)}

def extract_email_body(payload):
    """Extracts and decodes the email body."""
    if "parts" in payload:
        for part in payload["parts"]:
            if part["mimeType"] == "text/plain":
                body_data = part["body"].get("data", "")
                if body_data:
                    return base64.urlsafe_b64decode(body_data).decode("utf-8", errors="ignore")
    return "No content available"

def extract_sender_name(from_header):
    """Extracts sender name from 'From' header."""
    match = re.match(r'^(.*?)(<.*?>)$', from_header)
    return match.group(1).strip('"') if match else from_header
