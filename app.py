from flask import Flask, render_template, request, redirect, url_for
from db import get_important_senders, update_sender_priority, remove_sender_priority
from gmail_service import get_emails, get_email_content, prioritize_emails  # Import prioritize_emails

app = Flask(__name__)

@app.route('/')
def index():
    """Fetch emails, prioritize them, and render the inbox."""
    emails = get_emails()
    emails = prioritize_emails(emails)  # Assign priorities

    return render_template("index.html", emails=emails)

@app.route('/select_important_senders', methods=['GET', 'POST'])
def select_important_senders():
    """Allow users to mark/unmark important senders."""
    if request.method == 'POST':
        selected_senders = set(request.form.getlist('senders'))
        current_senders = set(get_important_senders().keys())

        # Add new important senders
        for sender in selected_senders:
            update_sender_priority(sender, 5)  

        # Remove unchecked senders
        for sender in current_senders - selected_senders:
            remove_sender_priority(sender)

        return redirect(url_for('index'))  

    emails = get_emails()
    unique_senders = list(set(email['from'] for email in emails))
    important_senders = get_important_senders()

    return render_template("set_priority.html", senders=unique_senders, important_senders=important_senders)

@app.route('/email/<email_id>')
def view_email(email_id):
    """Displays full content of an email."""
    email_content = get_email_content(email_id)
    return render_template("email.html", email=email_content)

if __name__ == '__main__':
    app.run(debug=True)
