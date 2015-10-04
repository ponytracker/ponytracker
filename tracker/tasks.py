from celery import shared_task

from django.core import mail
from django.core.mail import EmailMessage


@shared_task
def send_mails(mails):
    messages = []
    for subject, message, from_addr, dests, reply_to, headers in mails:
        messages += [EmailMessage(subject, message, from_addr, dests, reply_to=reply_to, headers=headers)]
    with mail.get_connection() as connection:
        connection.send_messages(messages)
