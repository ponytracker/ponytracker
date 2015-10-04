from celery import shared_task

from django.core import mail
from django.core.mail import EmailMessage


@shared_task
def send_mails(mails):
    messages = []
    for subject, message, from_addr, dests, headers in mails:
        messages += [EmailMessage(subject, message, from_addr, dests, headers=headers)]
    with mail.get_connection() as connection:
        connection.send_messages(messages)
