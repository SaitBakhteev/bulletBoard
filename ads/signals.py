from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Response

@receiver(post_save, sender=Response)
def notify_about_response(sender, instance, created, **kwargs):
    if created:
        subject = f'Новый отклик на ваше объявление "{instance.ad.title}"'
        message = f'Пользователь {instance.author} оставил отклик: {instance.text}'
        send_mail(subject, message, 'admin@mmorpg.com', [instance.ad.author.email])

    elif instance.is_accepted and not kwargs.get('raw', False):
        subject = f'Ваш отклик принят!'
        message = f'Автор объявления "{instance.ad.title}" принял ваш отклик.'
        send_mail(subject, message, 'admin@mmorpg.com', [instance.author.email])