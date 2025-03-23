import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services import inventory_service as inv_serv
import pandas as pd

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

def generate_purchase_alerts(df: pd.DataFrame):
    # Join the updated inventory to the dosage_data table
    df = df.merge(inv_serv.get_dosage_data(), on=['supplement_id', 'user_id'], how='left')
    # print(df)

    # Look at the inventory data qty_remaining and filter for those than are less than or equal to the dosage_data.dosage_per_day value
    df = df[df['qty_remaining'] <= df['reorder_threshold']]
    print(df)

    if df.empty:
        print("No purchase alerts needed")
        return
    
    # activate alert for the user if the df is not empty
    supplement_data = inv_serv.get_supplement_data()
    df = df.merge(supplement_data, on='id', how='left')
    # print(f'Alert! You need to replace supplements: {df["supplement_name"].unique()}')

    # Calculate dosages remaining per supplement row.
    df['dosages_remaining'] = df['qty_remaining'] / df['dosage_per_day']

    # Group by supplement name. (You might use mean(), sum(), or min() depending on your business logic.
    # Here, we'll assume each supplement appears only once after the DISTINCT query,
    # or that using the average is acceptable.)
    grouped = df.groupby('supplement_name')['dosages_remaining'].mean()

    # Build the email message.
    email_subject = "Supplement Replacement Alert"
    email_message = "Dear User,\n\n"
    email_message += "Our records indicate that the following supplements need to be replaced:\n\n"

    for supplement, dosages in grouped.items():
        email_message += f"- {supplement}: {dosages:.0f} dosages remaining\n"

    email_message += "\nPlease consider reordering them at your earliest convenience.\n\n"
    email_message += "Best regards,\nYour Supplement Inventory Team"

    send_email(subject=email_subject, body=email_message, recipient_emails=["regan@slantresearch.com"])

    return df

def send_email(subject: str, body: str, recipient_emails: list):
    """
    Sends an email using Gmail's SMTP with SSL.
    
    Requirements:
    - Set the following environment variables:
        GMAIL_USER: your full Gmail address (e.g. yourname@gmail.com)
        GMAIL_APP_PASSWORD: your Gmail App Password (generated in your Google Account settings)
    
    Parameters:
    - subject: Subject of the email.
    - body: Body of the email (plain text).
    - recipient_emails: List of recipient email addresses.
    """
    # Retrieve credentials from environment variables
    load_dotenv()
    sender_email = os.getenv('GMAIL_USER')
    app_password = os.getenv('GMAIL_APP_PASSWORD')
    
    if not sender_email or not app_password:
        raise ValueError("Gmail credentials not set. Please set GMAIL_USER and GMAIL_APP_PASSWORD environment variables.")
    
    # Create a multipart email message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ", ".join(recipient_emails)
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    
    # Connect securely to Gmail's SMTP server using SSL
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, app_password)
        server.sendmail(sender_email, recipient_emails, message.as_string())
    
    print("Email sent successfully!")