from django.urls import path, include


from rest_framework import routers
from rest_framework_simplejwt.views import (
                                             TokenObtainPairView, TokenRefreshView 
                                            )


from account_API import views

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', views.UserApiViewSet)
# router.register(r'users/<int:pk>/', views.UserDetailApiView.as_view())

urlpatterns = [
    path('', include(router.urls)),
    path('users/<int:pk>/', views.UserDetailApiView.as_view()),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
