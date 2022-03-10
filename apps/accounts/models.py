from django.contrib.auth.hashers import make_password
from django.contrib.gis.db import models
from django.utils.crypto import get_random_string
from django_lifecycle import AFTER_CREATE, hook, BEFORE_UPDATE
from apps.utils.models import BaseModel, BaseModelUser
from apps.utils.redis import client as redis


class Account(BaseModelUser):
    phone = models.CharField(
        max_length=15
    )

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    @hook(AFTER_CREATE)
    def on_create(self):
        if redis.get_json('setup').get('disable_user_when_register'):
            self.disable()
        self.set_raw_password()

    @hook(BEFORE_UPDATE)
    def on_update(self):
        self.set_raw_password()

