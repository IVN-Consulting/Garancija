from __future__ import absolute_import, unicode_literals
import celery
from django.core.mail import send_mail


@celery.shared_task
def add(x, y):
    return x+y


@celery.shared_task
def send_async_mail(subject, message, from_email, recipient_list):
    send_mail(subject, message, from_email, recipient_list)
