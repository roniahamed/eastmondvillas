import requests
from django.conf import settings
from django.core.mail import send_mail


def send_email(subject, recipient_list, message=None, template=None):

    if template:
        message = template

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        html_message=template,
        recipient_list=recipient_list,
        fail_silently=False,
    )
    