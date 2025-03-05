import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Your Gmail credentials
GMAIL_USER = "crazytrazy2004@gmail.com"
GMAIL_APP_PASSWORD = "nehn ghfm bsvk rcpr"

def send_email(to_email, subject, body):
    """Send an email using Gmail SMTP."""
    msg = MIMEMultipart()
    msg["From"] = GMAIL_USER
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        # Connect to Gmail SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_USER, to_email, msg.as_string())
        server.quit()
        print(f"✅ Email sent to {to_email}")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

# Example Usage
if __name__ == "__main__":
    send_email("recipient@example.com", "Today's Workout", "Here is your workout for today!")
