from celery import shared_task

from django.core import mail
from django.core.mail import EmailMultiAlternatives


@shared_task
def send_mails(mails):
    messages = []
    for subject, message, from_addr, dests, reply_to, headers in mails:
        text_message, html_message = message
        msg = EmailMultiAlternatives(subject, text_message, from_addr, dests, reply_to=reply_to, headers=headers)
        msg.attach_alternative(html_message, 'text/html')
        messages += [msg]
    with mail.get_connection() as connection:
        connection.send_messages(messages)
