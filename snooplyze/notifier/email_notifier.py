import smtplib
from email.message import EmailMessage
from notifier import Notifier


class EmailNotifier(Notifier):
    """
    EmailNotifier is a class for sending email notifications about new content updates.
    Attributes:
        email_address (str): The sender's email address.
        email_password (str): The password for the sender's email account.
        recipients (str): The recipient(s) email address(es).
        page_name (str): The name of the page being monitored.
        content_time (str): The timestamp of the new content.
        page_url (str): The URL of the page being monitored.
        subject (str): The subject of the email notification.
    Methods:
        __init__(email_address, email_password, recipients, page_name, content_time, page_url):
            Initializes the EmailNotifier with email credentials and page details.
        set_subject(subject):
            Sets the subject for the email notification.
        set_recipients(recipients):
            Sets the recipients for the email notification.
        notify(message):
            Sends an email notification with the provided message and page details.
            Uses an HTML template for the email body and sends the email via Gmail's SMTP server.
    """

    def __init__(self, email_address: str, email_password: str, recipients: str, page_name: str, content_time: str, page_url: str):
        self.email_address = email_address
        self.email_password = email_password
        self.recipients = recipients
        self.page_name = page_name
        self.content_time = content_time
        self.page_url = page_url

    def set_subject(self, subject: str):
        self.subject = subject

    def set_recipients(self, recipients: str):
        self.recipients = recipients


    def notify(self, message):

        from string import Template
        import os

        base_dir = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(base_dir, "email_template.html")

        with open(template_path) as f:
            html_template = Template(f.read())

            html = html_template.substitute(
                page = self.page_name,
                contenttime = self.content_time,
                message = message,
                link = self.page_url
            )

        # Create the message
        msg = EmailMessage()
        msg['Subject'] = f"[Snooplyze] New content for Page: {self.page_name} at {self.content_time}"
        msg['From'] = self.email_address
        msg['To'] = self.recipients
        #msg['To'] = ', '.join(['user1@example.com', 'user2@example.com'])
        msg.set_content(message)
        msg.add_alternative(html, subtype = "html")

        # Send the email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(self.email_address, self.email_password)
            smtp.send_message(msg)

        print(f"🔔 Email Notification for [{self.page_name}] sent successfully.")

