from django.urls import path, include
from rest_framework import routers
from . import views
from . import viewsets

router = routers.DefaultRouter()
router.register(r'users', viewsets.AccountAuthViewSet)
router.register(r'register', viewsets.AccountRegisterViewSet)

urlpatterns = [
    path('', include(router.urls))
]
