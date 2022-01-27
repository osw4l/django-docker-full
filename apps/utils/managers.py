from django.db import models


class ModelModelQuerySet(models.QuerySet):
    def all(self):
        return self.filter(deleted=False)

    def deleted(self):
        return self.filter(deleted=True)


class ModelModelManager(models.Manager):
    def get_queryset(self):
        return ModelModelQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().all()

    def deleted(self):
        return self.get_queryset().deleted()

