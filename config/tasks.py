from __future__ import absolute_import, unicode_literals
from config.celery import app
from django.core.mail import send_mail
from garancija.models import Warranty


@app.task
def add(x, y):
    return x + y


@app.task
def num_of_warranties():
    warranties = len(Warranty.objects.all())
    return warranties


@app.task
def all_warranties():
    warranties = Warranty.objects.all()
    return warranties


@app.task
def send_async_mail(subject, message, from_email, recipient_list):
    send_mail(subject, message, from_email, recipient_list)
