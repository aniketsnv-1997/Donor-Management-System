from requests import Response, post
from flask import url_for, request, redirect
from flask_mail import Message
from dms import mail


class AutomaticEmailException(Exception):
    def __init__(self, message: str):
        super.__init__(message)


class AutomaticEmail:
    """
    This class consists of the following methods which are used to send automatic emails

    send_email_of_user_registration(email_address, name, password, role_name, project name) - Responsible to notify an
    newly registered user through an email
    """
    MAILGUN_DOMAIN = "sandbox7c7a5537dd414ec2b57f3e26ce084208.mailgun.org"
    MAILGUN_API_KEY = "0bde311ed42585b3c94ad8d5ef0f5d28-1b6eb03d-0e5a3b97"
    FROM_TITLE = "Vivekanand Seva Mandal DMS Communications"
    FROM_EMAIL = "postmaster@sandbox7c7a5537dd414ec2b57f3e26ce084208.mailgun.org"

    @classmethod
    def send_email(cls, email_address: str, subject: str, body: str) -> Response:
        if cls.MAILGUN_API_KEY is None:
            raise AutomaticEmailException("Failed to load the MAILGUN_API_KEY")

        if cls.MAILGUN_DOMAIN is None:
            raise AutomaticEmailException("Failed to load the MAILGUN_DOMAIN")

        response = post(
            f"https://api.mailgun.net/v3/{cls.MAILGUN_DOMAIN}/messages",
            auth=("api", cls.MAILGUN_API_KEY),
            data={
                "from": f"{cls.FROM_TITLE} <{cls.FROM_EMAIL}>",
                "to": email_address,
                "subject": subject,
                "text": body
            }
        )

        if response.status_code != 200:
            raise AutomaticEmailException("Failed to send the email, User Registration Failed!")

        return response
