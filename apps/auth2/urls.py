from django.urls import path, include
from rest_framework import routers
from . import views
from . import viewsets

router = routers.DefaultRouter()
router.register(r'users', viewsets.CompanyUserAuthViewSet)
router.register(r'register', viewsets.CompanyUserRegisterViewSet)

urlpatterns = [
    path('', include(router.urls))
]
