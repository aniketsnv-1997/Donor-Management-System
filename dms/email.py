from flask_mail import Message
from dms import mail


def send_email_of_user_registration(sender, receiver, text_body):
    msg = Message("DMS Account Creation Email", sender=sender, recipients=receiver)
    msg.body = text_body
    mail.send(msg)
    return 1


def send_email_of_donor_registration(sender, receiver, text_body):
    msg = Message("Welcome to the VSM Family", sender=sender, recipients=receiver)
    msg.body = text_body
    mail.send(msg)


def send_email_of_birthday(sender, receiver, text_body):
    msg = Message("Birthday Wishes!", sender=sender, recipients=receiver)
    msg.body = text_body
    mail.send(msg)


def send_email_of_donation(subject, sender, receiver, text_body):
    msg = Message(subject, sender=sender, recipients=receiver)
    msg.body = text_body
    mail.send(msg)