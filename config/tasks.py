from __future__ import absolute_import, unicode_literals
from config.celery import app
from django.core.mail import send_mail


@app.task
def add(x, y):
    return x + y


@app.task
def send_async_mail(subject, message, from_email, recipient_list):
    send_mail(subject, message, from_email, recipient_list)