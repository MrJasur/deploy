#use celery 
from django.core.mail import send_mail
from conf.celery import app

@app.task()
def send_email(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        'coderkr.llc@gmail.com',
        recipient_list,
    )