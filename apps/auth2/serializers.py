from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import CompanyUser
from apps.utils.shortcuts import get_object_or_none
from apps.utils.exceptions import EmailValidationError


class UserResetPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=2, max_length=64)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class UserResetPasswordCodeSerializer(UserResetPasswordSerializer):
    code = serializers.CharField(max_length=6)


class UserResetPasswordSetPasswordSerializer(UserResetPasswordCodeSerializer):
    password = serializers.CharField(min_length=6)


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=2, max_length=64)
    password = serializers.CharField()

    def update(self, instance, validated_data):
        pass

    def validate(self, data):
        user = authenticate(username=data.get('username'), password=data.get('password'))
        if not user:
            raise serializers.ValidationError({
                'error': 'Las credenciales no son válidas'
            })
        if not hasattr(user, 'companyuser'):
            raise serializers.ValidationError({
                'error': 'No tiene permisos para entrar aquí'
            })
        self.context['user'] = user
        return data

    def create(self, data):
        user = self.context['user']
        token = get_object_or_none(Token, user=user)
        if token:
            token.delete()
        token, created = Token.objects.update_or_create(user=user)
        user = CompanyUserSerializer(user.companyuser)
        return user.data, token.key


class CheckEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        if CompanyUser.objects.filter(email=data.get('email')):
            raise EmailValidationError()
        return data

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class CompanyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyUser
        fields = (
            'uuid',
            'username',
            'phone',
            'email',
            'first_name',
            'last_name',
            'role',
            'is_active'
        )
        extra_kwargs = {
            'uuid': {
                'read_only': True
            }
        }


class CompanyUserRegisterSerializer(CompanyUserSerializer):
    class Meta(CompanyUserSerializer.Meta):
        fields = CompanyUserSerializer.Meta.fields + ('raw_password',)
        extra_kwargs = {
            'raw_password': {
                'write_only': True
            },
            'role': {
                'read_only': True
            },
            'code': {
                'read_only': True
            },
            'is_active': {
                'read_only': True
            }
        }
