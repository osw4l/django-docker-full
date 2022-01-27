from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.utils.crypto import get_random_string
from django_lifecycle import AFTER_CREATE, hook, BEFORE_UPDATE
from apps.utils.models import BaseModel, BaseModelUser
from .choices import ROLES, CUSTOMER
from apps.utils.redis import client as redis


class CompanyUser(BaseModelUser, User):
    validate_code = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )
    phone = models.CharField(
        max_length=15
    )
    role = models.CharField(
        max_length=20,
        choices=ROLES,
        default=CUSTOMER,
        blank=True,
        null=True
    )
    raw_password = models.CharField(
        max_length=255
    )
    reset_password_code = models.CharField(
        max_length=6,
        blank=True,
        null=True
    )
    deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Company User'
        verbose_name_plural = 'Company Users'

    @hook(AFTER_CREATE)
    def on_create(self):
        if redis.get_json('setup').get('disable_user_when_register'):
            self.disable()
        self.set_raw_password()

    @hook(BEFORE_UPDATE)
    def on_update(self):
        self.set_raw_password()

    def set_raw_password(self):
        if self.raw_password:
            password = make_password(self.raw_password)
            self.__class__.objects.filter(id=self.id).update(
                password=password
            )

    def reset_password(self, password):
        self.raw_password = password
        self.reset_password_code = None
        self.save(update_fields=['raw_password', 'reset_password_code'])

    def generate_reset_password_code(self):
        self.reset_password_code = get_random_string(length=6, allowed_chars='0123456789')
        self.save(update_fields=['reset_password_code'])

    def logical_erase(self):
        self.is_active = False
        self.deleted = True
        self.save(update_fields=['is_active', 'deleted'])
        return {
            'deleted': self.deleted,
            'disabled': not self.is_active
        }

    def disable(self):
        self.is_active = False
        self.save(update_fields=['is_active'])
        return {
            'disabled': self.is_active
        }

    def enable(self):
        self.is_active = True
        self.save(update_fields=['is_active'])
        return {
            'disabled': self.is_active
        }

    def restore(self):
        self.is_active = True
        self.deleted = False
        self.save(update_fields=['is_active', 'deleted'])

