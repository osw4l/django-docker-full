from django import forms
from .models import Account


class AccountAdminForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'validate_code',
            'phone',
            'role',
            'deleted',
            'reset_password_code',
            'raw_password'
        )