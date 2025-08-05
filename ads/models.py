from django.db import models
from django.contrib.auth.models import User

from ckeditor.fields import RichTextField  # Для WYSIWYG

CATEGORIES = (
    ('tanks', 'Танки'),
    ('heals', 'Хилы'),
    ('dd', 'ДД'),
    ('merchants', 'Торговцы'),
    ('guildmasters', 'Гилдмастеры'),
    ('questgivers', 'Квестгиверы'),
    ('blacksmiths', 'Кузнецы'),
    ('tanners', 'Кожевники'),
    ('potionmakers', 'Зельевары'),
    ('spellmasters', 'Мастера заклинаний'),
)

class Ad(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name="Заголовок объявления")
    content = RichTextField(verbose_name="Содержание объявления, включая медиаконтент")  # WYSIWYG-поле
    category = models.CharField(max_length=20, choices=CATEGORIES, verbose_name="Категория объявления")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Response(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Текст отклика')
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Response to {self.ad.title}"


# Подписчики на рассылки вышедших объявлений
class Subscriber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.JSONField(max_length=20, choices=CATEGORIES)


# Класс для менеджеров доски объявлений, для которых устанавливаются особые права
class Manager(models.Model):
    manager = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        permissions = [('can_send_mass_email', 'can_send_mass_email')]
