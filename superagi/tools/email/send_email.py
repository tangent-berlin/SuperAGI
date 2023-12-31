import imaplib
import smtplib
import time
from email.message import EmailMessage
from typing import Type

from pydantic import BaseModel, Field

from superagi.config.config import get_config
from superagi.helper.imap_email import ImapEmail
from superagi.tools.base_tool import BaseTool


class SendEmailInput(BaseModel):
    to: str = Field(
        ...,
        description="Email Address of the Receiver, default email address is 'example@example.com'",
    )
    subject: str = Field(..., description="Subject of the Email to be sent")
    body: str = Field(..., description="Email Body to be sent")


class SendEmailTool(BaseTool):
    name: str = "Send Email"
    args_schema: Type[BaseModel] = SendEmailInput
    description: str = "Send an Email"

    def _execute(self, to: str, subject: str, body: str) -> str:
        email_sender = get_config("EMAIL_ADDRESS")
        email_password = get_config("EMAIL_PASSWORD")
        if email_sender == "" or email_sender.isspace():
            return "Error: Email Not Sent. Enter a valid Email Address."
        if email_password == "" or email_password.isspace():
            return "Error: Email Not Sent. Enter a valid Email Password."
        message = EmailMessage()
        message["Subject"] = subject
        message["From"] = email_sender
        message["To"] = to
        signature = get_config("EMAIL_SIGNATURE")
        if signature:
            body += f"\n{signature}"
        message.set_content(body)
        draft_folder = get_config("EMAIL_DRAFT_MODE_WITH_FOLDER")
        if message["To"] == "example@example.com" or draft_folder:
            conn = ImapEmail().imap_open(draft_folder, email_sender, email_password)
            conn.append(
                draft_folder,
                "",
                imaplib.Time2Internaldate(time.time()),
                str(message).encode("UTF-8"),
            )
            return f"Email went to {draft_folder}"
        else:
            smtp_host = get_config("EMAIL_SMTP_HOST")
            smtp_port = get_config("EMAIL_SMTP_PORT")
            with smtplib.SMTP(smtp_host, smtp_port) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.login(email_sender, email_password)
                smtp.send_message(message)
                smtp.quit()
            return f"Email was sent to {to}"
