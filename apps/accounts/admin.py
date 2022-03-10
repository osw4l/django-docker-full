from django.contrib import admin

from .forms import AccountAdminForm
from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = [
        'uuid',
        'username',
        'date_joined',
        'phone',
        'role',
        'is_active',
        'deleted',
    ]
    list_display_links = [
        'uuid'
    ]
    form = AccountAdminForm
    actions = [
        'enable',
        'disable',
        'restore',
        'logical_erase'
    ]
    search_fields = [
        'email',
        'username',
        'first_name',
        'last_name'
    ]

    def enable(self, request, queryset):
        for ad in queryset:
            ad.enable()

    def disable(self, request, queryset):
        for ad in queryset:
            ad.disable()

    def logical_erase(self, request, queryset):
        for ad in queryset:
            ad.logical_erase()

    def restore(self, request, queryset):
        for ad in queryset:
            ad.restore()

    enable.description = 'Enable User(s)'
    disable.description = 'Disable User(s)'
    logical_erase.description = 'Delete User(s)'
    restore.description = 'Restore User(s)'

