from django.conf import settings
if 'djcelery' in settings.INSTALLED_APPS:
    from ponytracker.celery import app as celery_app
