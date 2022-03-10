import uuid
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from .managers import ModelModelManager
from django_lifecycle import LifecycleModel
from .choices import ROLES, CUSTOMER


class BaseModel(LifecycleModel):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False, editable=False)
    objects = ModelModelManager()

    class Meta:
        abstract = True

    def logical_erase(self):
        self.deleted = True
        self.save(update_fields=['deleted'])
        return {
            'deleted': self.deleted
        }


class BaseModelUser(BaseModel, User):
    objects = UserManager()
    validate_code = models.CharField(
        max_length=10,
        blank=True,
        null=True
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
        abstract = True

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


class BaseNameModel(BaseModel):
    name = models.CharField(
        max_length=50,
        unique=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
