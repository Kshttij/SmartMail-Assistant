def classify_email(text):
    """
    A simple rule-based classifier that returns:
      - 5 if any high-priority keyword is found,
      - 3 if any moderate-priority keyword is found,
      - 1 otherwise.
    """
    text = text.lower()

    high_priority_keywords = [
        "urgent", "immediate", "final reminder", 
        "action required", "security alert", "deadline", 
        "critical", "warning"
    ]
    moderate_priority_keywords = [
        "important", "reminder", "due soon"
    ]
    
    for kw in high_priority_keywords:
        if kw in text:
            return 5  # High priority

    for kw in moderate_priority_keywords:
        if kw in text:
            return 3  # Medium priority

    return 1  # Low priority if nothing matches

if __name__ == "__main__":
    # Test cases
    test_emails = [
        "Urgent: Your bank account has been compromised. Immediate action required.",
        "Final Reminder: Your assignment deadline is tomorrow!",
        "Important: Meeting rescheduled.",
        "Limited-time offer on electronics."
    ]
    
    for email in test_emails:
        print("Email:", email)
        print("Priority Score:", classify_email(email))
        print("-" * 50)
