from celery import shared_task

from django.core.mail import EmailMessage


@shared_task
def send_mail(subject, message, from_addr, dests, headers={}):
    mail = EmailMessage(subject, message, from_addr, dests, headers=headers)
    mail.send()
