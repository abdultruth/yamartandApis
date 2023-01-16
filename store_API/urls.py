from django.urls import path, include
from rest_framework import routers


from store_API import views

router = routers.DefaultRouter()
router.register(r'products', views.ProductApiViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
