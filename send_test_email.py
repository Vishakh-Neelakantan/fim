import smtplib
from email.mime.text import MIMEText

# Create a test email message
msg = MIMEText("This is a test email.")
msg["Subject"] = "Test Email"
msg["From"] = "sender@example.com"
msg["To"] = "recipient@example.com"

try:
    print("Attempting to send email...")
    # Connect to the local SMTP server
    with smtplib.SMTP("localhost", 1025) as server:
        server.sendmail("sender@example.com", ["recipient@example.com"], msg.as_string())
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
