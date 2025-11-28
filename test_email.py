"""Test script to verify email notification setup"""
import os
from dotenv import load_dotenv
from CEACStatusBot import EmailNotificationHandle

# Load environment variables
load_dotenv()

FROM = os.getenv("FROM")
TO = os.getenv("TO")
PASSWORD = os.getenv("PASSWORD")
SMTP = os.getenv("SMTP", "")

if not all([FROM, TO, PASSWORD]):
    print("❌ Email configuration missing!")
    print(f"FROM: {FROM}")
    print(f"TO: {TO}")
    print(f"PASSWORD: {'***' if PASSWORD else 'NOT SET'}")
    print(f"SMTP: {SMTP}")
    exit(1)

print("✅ Email configuration found:")
print(f"FROM: {FROM}")
print(f"TO: {TO}")
print(f"SMTP: {SMTP}")
print("\n🔄 Sending test email...")

# Create test notification data matching the expected format
test_data = {
    "success": True,
    "visa_type": "NONIMMIGRANT VISA APPLICATION",
    "status": "Test - Email Configuration Working!",
    "case_created": "28-Nov-2025",
    "case_last_updated": "28-Nov-2025",
    "description": "This is a test email from CEACStatusBot to verify your email configuration is working properly.",
    "application_num": "***",
    "application_num_origin": os.getenv("NUMBER", "TEST123"),
    "number": os.getenv("NUMBER", "TEST"),
    "location": os.getenv("LOCATION", "TEST LOCATION")
}

try:
    email_handle = EmailNotificationHandle(FROM, TO, PASSWORD, SMTP)
    email_handle.send(test_data)
    print(f"\n✅ Test email sent successfully to {TO}!")
    print("📧 Check your inbox (and spam folder) for the test email.")
except Exception as e:
    print(f"\n❌ Error sending email: {e}")
    print("\nPossible issues:")
    print("1. Check if you're using an App Password (not regular password) for Gmail")
    print("2. Verify 2-Step Verification is enabled on your Gmail account")
    print("3. Check SMTP server settings")
    print("4. Verify your internet connection")
