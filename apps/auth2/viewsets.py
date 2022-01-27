from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.utils.permissions import IsCompanyUser, IsRegisterEnabled
from .models import CompanyUser
from apps.utils.viewsets import OwnerModelViewSet
from .serializers import (
    CompanyUserSerializer,
    UserLoginSerializer,
    UserResetPasswordCodeSerializer,
    UserResetPasswordSerializer,
    UserResetPasswordSetPasswordSerializer,
    CompanyUserRegisterSerializer, CheckEmailSerializer
)



class CompanyUserRegisterViewSet(viewsets.GenericViewSet):
    serializer_class = CompanyUserSerializer
    queryset = CompanyUser.objects.filter(deleted=False)

    @action(detail=False,
            methods=['POST'],
            permission_classes=[AllowAny],
            serializer_class=CheckEmailSerializer)
    def check_email(self, request):
        """User check email."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response()

    @action(detail=False,
            methods=['POST'],
            permission_classes=[AllowAny, IsRegisterEnabled],
            serializer_class=CompanyUserRegisterSerializer)
    def register(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)


class CompanyUserAuthViewSet(viewsets.GenericViewSet):
    serializer_class = CompanyUserSerializer
    queryset = CompanyUser.objects.filter(deleted=False)
    permission_classes = [
        IsAuthenticated,
        IsCompanyUser,
    ]

    @action(detail=False,
            methods=['POST'],
            permission_classes=[AllowAny],
            serializer_class=UserLoginSerializer)
    def login(self, request):
        """User sign in."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        return Response({
            'user': user,
            'token': token
        })

    @action(detail=False,
            methods=['POST'],
            permission_classes=[AllowAny],
            serializer_class=UserResetPasswordSerializer)
    def send_reset_code(self, request):
        username = request.data.get('username')
        user = get_object_or_404(CompanyUser, username=username)
        user.generate_reset_password_code()
        return Response({
            "success": True
        })

    @action(detail=False,
            permission_classes=[AllowAny],
            methods=['POST'],
            serializer_class=UserResetPasswordCodeSerializer)
    def check_reset_password_code(self, request):
        username = request.data.get('username')
        reset_password_code = request.data.get('code')
        get_object_or_404(CompanyUser, username=username, reset_password_code=reset_password_code)
        return Response({
            "success": True
        })

    @action(detail=False,
            methods=['POST'],
            permission_classes=[AllowAny],
            serializer_class=UserResetPasswordSetPasswordSerializer)
    def set_new_password(self, request):
        username = request.data.get('username')
        code = request.data.get('code')
        password = request.data.get('password')
        user = get_object_or_404(CompanyUser, username=username, reset_password_code=code)
        user.reset_password(password)
        return Response({
            "success": True
        })

    @action(detail=False, methods=['GET'])
    def detail_user(self, request):
        serializer = self.serializer_class(request.user.companyuser)
        return Response(serializer.data)

    @action(detail=False, methods=['PUT'])
    def update_user(self, request):
        serializer = self.serializer_class(request.user.companyuser, request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)


class CompanyUserOwnerViewSet(OwnerModelViewSet):
    serializer_class = CompanyUserRegisterSerializer
    queryset = CompanyUser.objects.filter(deleted=False)
    search_fields = ('username', 'first_name', 'last_name',)

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.companyuser.company)

    @action(detail=True, methods=['DELETE'], serializer_class=None)
    def delete(self, request, uuid=None):
        result = self.get_object().logical_erase()
        return Response(result)

    @action(detail=True, methods=['POST'], serializer_class=None)
    def disable(self, request, uuid=None):
        result = self.get_object().disable()
        return Response(result)

    @action(detail=True, methods=['POST'], serializer_class=None)
    def enable(self, request, uuid=None):
        result = self.get_object().enable()
        return Response(result)

