from django.db import models
from django.contrib.auth.models import AbstractUser


class Chef(AbstractUser):
    is_activated = models.BooleanField(verbose_name='Активен', default=True, db_index=True)
    send_messages = models.BooleanField(verbose_name='Получать ли рассылки', default=True)

    class Meta(AbstractUser.Meta):
        pass

