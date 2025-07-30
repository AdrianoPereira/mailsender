# MailSender

A Python script to send personalized emails with attachments to multiple recipients using Gmail SMTP and Google App Password.

## Features

- Send emails with personalized bodies and attachments to a list of contacts from a CSV file.
- Securely load configuration from environment variables via a `.env` file.
- Use Gmail SMTP with TLS for secure email delivery.

## Prerequisites

- Python 3.6 or higher
- A Gmail account with 2-Step Verification enabled
- A generated Google App Password for SMTP authentication

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```
2. (Optional) Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Create a `.env` file in the root of the project with the following variables:

```ini
SENDER_EMAIL=your-email@gmail.com      # Your Gmail address
APP_PASSWORD=your-app-password        # Your 16-character Google App Password
EMAIL_SUBJECT=Your email subject      # Subject line for the sent emails
CSV_FILE_PATH=path/to/contacts.csv    # Path to your CSV file containing contacts
```

### How to Generate a Google App Password

1. Sign in to your Google Account and navigate to **Security**: [https://myaccount.google.com/security](https://myaccount.google.com/security)
2. Under **"Signing in to Google"**, ensure **2-Step Verification** is enabled.
3. Click on **App passwords**.
4. In the **Select app** dropdown, choose **Mail**, then select your device or **Other (Custom name)**, e.g., "Email Script".
5. Click **Generate**.
6. Copy the 16-character app password and place it in your `.env` file as the value for `APP_PASSWORD`.

## Usage

Run the script to send emails to all contacts listed in the CSV file:

```bash
python send_emails.py
```

The CSV file should have the following format (with a header row):

```csv
name,email,attachment_path
John Doe,john.doe@example.com,/path/to/file1.pdf
Jane Smith,jane.smith@example.com,/path/to/file2.pdf
```

## Error Handling & Troubleshooting

- **FileNotFoundError**: Ensure the paths in `CSV_FILE_PATH` and each `attachment_path` are correct.
- **SMTPAuthenticationError**: Verify your `SENDER_EMAIL` and `APP_PASSWORD`. Make sure your App Password is active and 2-Step Verification is set up.
- **Other Exceptions**: Review the console output for detailed error messages.

## License

This project is licensed under the MIT License. Feel free to modify and distribute.

