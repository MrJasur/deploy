from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from users.models import CustomUserModel

@receiver(post_save, sender = CustomUserModel)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
                "Welcome to Goodreads Clone",
                f"Hi, {instance.username}. Welcome to Goodreads Clone. Enjoy the books and reviews",
                'jasurbekodilovn@gmail.com',
                [instance.email]
            )