from django import forms
from .models import CompanyUser


class CompanyUserAdminForm(forms.ModelForm):
    class Meta:
        model = CompanyUser
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