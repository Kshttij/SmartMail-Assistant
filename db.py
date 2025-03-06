import mysql.connector
from gmail_auth import get_authenticated_user_email  # Fetch logged-in user's email

db_config = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "Goldline123",
    "database": "gmail_assistant"
}

def get_db_connection():
    """Establish a connection to the database."""
    return mysql.connector.connect(**db_config)

def get_important_senders():
    """Fetch important senders for the authenticated user."""
    user_email = get_authenticated_user_email()
    if not user_email:
        return {}

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT sender_email FROM important_senders WHERE user_email = %s", (user_email,))
    
    senders = {row["sender_email"].lower(): 5 for row in cursor.fetchall()}  # Assign priority +5
    conn.close()
    return senders

def update_sender_priority(sender_email, priority):
    """Update or insert sender priority for the logged-in user."""
    user_email = get_authenticated_user_email()
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO important_senders (user_email, sender_email) VALUES (%s, %s) "
        "ON DUPLICATE KEY UPDATE sender_email = VALUES(sender_email)",
        (user_email, sender_email)
    )

    conn.commit()
    conn.close()

def remove_sender_priority(sender_email):
    """Remove a sender from the important senders list."""
    user_email = get_authenticated_user_email()
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM important_senders WHERE user_email = %s AND sender_email = %s",
        (user_email, sender_email)
    )

    conn.commit()
    conn.close()
