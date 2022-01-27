import uuid
from django.contrib.auth.models import UserManager
from django.contrib.gis.db import models
from .managers import ModelModelManager
from django_lifecycle import LifecycleModel


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


class BaseModelUser(BaseModel):
    objects = UserManager()

    class Meta:
        abstract = True


class BaseNameModel(BaseModel):
    name = models.CharField(
        max_length=50,
        unique=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
