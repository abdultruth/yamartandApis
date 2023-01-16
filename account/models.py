from distutils.command.upload import upload
import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from .managers import CustomUserManager

# Create your models here.
class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'A', _('admin')
        USER = 'U', _('user')

    username = None
    role = models.CharField(max_length=1, choices=Role.choices, default=Role.USER)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_no = models.IntegerField()
    joined_at = models.DateTimeField(auto_now_add=True)
    year_of_birth = models.DateField(null=True, editable=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','phone_no']
    
    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, add_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def get_absolute_url(self):
        return reverse('my-details', kwargs={'pk': id})
    
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        ordering = ['-joined_at']
        
        
        
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=100, blank=True)
    address_line_2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=20)
    profile_picture = models.ImageField(upload_to='userprofile', blank=True)
    state = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.first_name
    
    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'
    
    
        

    
