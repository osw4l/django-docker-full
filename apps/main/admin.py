from django.contrib import admin
from .models import Setup


@admin.register(Setup)
class SetupAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'allow_register',
        'disable_user_when_register',
        'http_server_on',
        'ws_server_on',
        'twilio_key'
    ]

    def has_add_permission(self, request):
        return Setup.objects.count() == 0

    def has_delete_permission(self, request, obj=None):
        return False
