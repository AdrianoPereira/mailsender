import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import csv
from dotenv import load_dotenv
load_dotenv()
import os

# --- CONFIGURATION ---
# --- You MUST change these variables ---

# Sender's email credentials
# IMPORTANT: Use an "App Password" generated from your Google Account, not your regular password.
sender_email = os.getenv("SENDER_EMAIL") # <-- Put your email here
email_password = os.getenv("APP_PASSWORD") # <-- Put your App Password here

# Email details
subject = os.getenv("EMAIL_SUBJECT") # <-- Put your email subject here

# File paths
csv_file_path = os.getenv("CSV_FILE_PATH") # <-- Path to your CSV file with contacts

# SMTP Server details for Gmail
smtp_server = "smtp.gmail.com"
smtp_port = 587 # For TLS connection

# --- END OF CONFIGURATION ---


def send_email(recipient_name, recipient_email, attachment_path):
    """
    Creates and sends an email to a single recipient.
    """
    try:
        # --- Create the email message ---
        # MIMEMultipart is a container for different parts of the email (text, attachment)
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient_email
        message["Subject"] = subject

        # --- Email Body ---
        # You can customize the body of the email here.
        # Using an f-string to personalize the email with the recipient's name.
        body = f"""
        Hi {recipient_name},

        This is an automated email sent via a Python script.
        Please find the document you requested in the attachment.

        Best regards,
        Adriano
        """
        # Attach the body of the email as MIMEText
        message.attach(MIMEText(body, "plain"))

        # --- Attach the PDF file ---
        # Open the PDF file in binary read mode ('rb')
        with open(attachment_path, "rb") as attachment:
            # Create a MIMEBase object for the attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode the attachment in base64
        encoders.encode_base64(part)

        # Add a header to the attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {attachment_path}",
        )

        # Attach the PDF part to the message
        message.attach(part)

        # --- Connect to the SMTP server and send the email ---
        # The 'with' statement ensures the connection is automatically closed
        print(f"Connecting to server...")
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Upgrade the connection to a secure TLS connection
            server.login(sender_email, email_password) # Login to your email account
            server.send_message(message) # Send the email

        print(f"Email successfully sent to {recipient_name} ({recipient_email})")
        return True

    except FileNotFoundError:
        print(f"Error: The file was not found. Check the paths for '{csv_file_path}' or '{attachment_path}'.")
        return False
    except smtplib.SMTPAuthenticationError:
        print("Error: SMTP authentication failed. Check your sender_email and email_password (App Password).")
        return False
    except Exception as e:
        print(f"An error occurred while sending to {recipient_email}: {e}")
        return False

# --- Main script execution ---
if __name__ == "__main__":
    print("Starting the email sending process...")

    # Read the CSV file to get contact details
    try:
        with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header row (e.g., "name,email")

            # Loop through each row in the CSV file
            for row in reader:
                recipient_name = row[0]
                recipient_email = row[1]
                attachment_path = row[2]
                print("-" * 20)
                send_email(recipient_name, recipient_email, attachment_path)

    except FileNotFoundError:
        print(f"CRITICAL ERROR: The CSV file '{csv_file_path}' was not found. The script cannot continue.")
    except Exception as e:
        print(f"An unexpected error occurred while reading the CSV file: {e}")

    print("-" * 20)
    print("Email sending process finished.")