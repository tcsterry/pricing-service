from requests import Response, post
import os
from typing import List


class MailgunException(Exception):
    def __init__(self, message: str):
        self.message = message


class Mailgun:
    FROM_TITLE = 'Pricing Service'
    FROM_EMAIL = 'Do-Not-Reply@sandbox51d3a75be9f5412b8436320839512271.mailgun.org'

    @classmethod
    def send_mail(cls, email: List[str], subject: str, text: str, html: str) -> Response:
        mailgun_api_key = os.environ.get('MAILGUN_API_KEY', None)
        mailgun_domain = os.environ.get('MAILGUN_DOMAIN', None)

        if mailgun_api_key is None:
            raise MailgunException('Failed to load Mailgun API key.')

        if mailgun_domain is None:
            raise MailgunException('Failed to load Mailgun Domain.')
        response = post(
            f"{mailgun_domain}/messages",
            auth=("api", mailgun_api_key),
            data={"from": f"{cls.FROM_TITLE} <{cls.FROM_EMAIL}>",
                  "to": email,
                  "subject": subject,
                  "text": text,
                  "html": html})

        if response.status_code != 200:
            print(response.json())
            raise MailgunException('An error occurred while sending e-mail.')
        return response
