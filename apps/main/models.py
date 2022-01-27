import json
from django.contrib.gis.db import models
from django_lifecycle import LifecycleModel, AFTER_CREATE, BEFORE_UPDATE, hook
from apps.utils.redis import client as redis


class Setup(LifecycleModel):
    allow_register = models.BooleanField(default=False)
    disable_user_when_register = models.BooleanField(default=True)
    http_server_on = models.BooleanField(default=True)
    ws_server_on = models.BooleanField(default=True)
    twilio_key = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    twilio_account_sid = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    twilio_auth_token = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    twilio_phone = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    email_host = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    email_host_user = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    from_email = models.EmailField(
        blank=True,
        null=True
    )
    payment_public_key = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    payment_private_key = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    payment_link_url = models.URLField(
        blank=True,
        null=True
    )
    frontend_url = models.URLField(
        blank=True,
        null=True
    )
    backend_url = models.URLField(
        blank=True,
        null=True
    )
    test_mode = models.BooleanField(default=True)


    class Meta:
        verbose_name = 'Setup'
        verbose_name_plural = 'Setup'

    def __str__(self):
        return 'Project Setup'

    def save(self, *args, **kwargs):
        if self.__class__.objects.all().count() <= 1:
            super().save(*args, **kwargs)

    def get_data(self):
        return json.dumps({
            'allow_register': self.allow_register,
            'disable_user_when_register': self.disable_user_when_register,
            'payment_private_key': self.payment_private_key,
            'test_mode': self.test_mode,
            'twilio_account_sid': self.twilio_account_sid,
            'twilio_auth_token': self.twilio_auth_token,
            'twilio_phone': self.twilio_phone,
            'email_host': self.email_host,
            'email_host_user': self.email_host_user,
            'from_email': self.from_email
        })

    @hook(AFTER_CREATE)
    def on_create(self):
        redis.set('setup', self.get_data())

    @hook(BEFORE_UPDATE)
    def on_update(self):
        redis.set('setup', self.get_data())


class Sms(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    phone = models.CharField(max_length=15)
    sms = models.TextField()
    success = models.BooleanField(null=True)
    source = models.CharField(
        max_length=20
    )
    data = models.JSONField()

    class Meta:
        verbose_name = 'Sms'
        verbose_name_plural = 'Sms'

    def set_status(self, status, data):
        self.success = status
        self.data = data
        self.save(update_fields=['success', 'data'])
