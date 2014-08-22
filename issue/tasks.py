from django.core.mail import send_mass_mail as django_send_mass_mail

from celery import shared_task


@shared_task
def send_mass_mail(datatuple):
    django_send_mass_mail(datatuple)
