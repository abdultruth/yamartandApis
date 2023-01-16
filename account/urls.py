from django.urls import path, include
from . import views


from account_API.urls import router


app_name = 'accounts'

urlpatterns = [
     path('register/', views.register, name='register'),
     path('login/', views.login, name='login'),
     path('logout/', views.logout, name='logout'),
     path('activate/<uidb64>/<token>/', views.activate, name='activate'),
     path('', views.dashboard, name='dashboard'),
     path('forgotpassword', views.forgotpassword, name='forgotpassword'),
     path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
     path('resetPassword/', views.resetPassword, name='resetPassword'),
     
     path('my_orders', views.my_orders, name='my_orders'),
     path('edit_profile', views.edit_profile, name='edit_profile'),
     path('change_password', views.change_password, name="change_password"),

]
