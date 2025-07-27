import smtplib
from email.message import EmailMessage
from notifier import Notifier


class EmailNotifier(Notifier):

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

