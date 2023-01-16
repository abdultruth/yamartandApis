from django import views
from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r'orders', views.OrderApiViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
