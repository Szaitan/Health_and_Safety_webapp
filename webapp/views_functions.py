from email.header import Header
from email.mime.text import MIMEText
import os
import smtplib


def register_send_email(customer_companies, name, last_name, company, email, customer_companies_emails_list):
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=os.environ.get("michal_mail"),
                         password=os.environ.get("google_app_access_password"))

        msg = MIMEText(
            f"Dear Mr/Mrs,\n\nPlease add me: {name} {last_name} from company: {company} as a user to {customer_companies} "
            f"customer group. My email: {email}",
            'plain', 'utf-8')
        msg['Subject'] = Header(f"{name} {last_name} ask to be added to {customer_companies}", 'utf-8').encode()
        connection.sendmail(from_addr=os.environ.get("michal_mail"), to_addrs=customer_companies_emails_list,
                            msg=msg.as_string())
