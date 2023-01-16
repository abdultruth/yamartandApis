from django.contrib import admin
from django.utils.html import format_html

from .models import CustomUser, UserProfile

class CustomerUserAdmin(admin.ModelAdmin):
     # field = '__all__'
     list_display = (
                     'email', 'first_name',
                     'last_name', 'last_login',
                     'date_joined', 'is_active'
                     )
     
     list_displsy_links = ('email', 'first_name', 'last_name')
     fieldsets = ()
     readonly_fields = ('last_login', 'date_joined')
     ordering = ('-date_joined',)
     
     

class UserProfileAdmin(admin.ModelAdmin):
     def thumbnail(self, object):
         return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.profile_picture.url))
     
     thumbnail.short_description = 'Profile Picture'
     list_display = ('thumbnail','user','city', 'state', 'country' )
     
admin.site.register(CustomUser, CustomerUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)