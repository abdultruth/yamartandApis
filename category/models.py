import uuid
from django.db import models
from django.urls import reverse

# Create your models here.
class Cartegory(models.Model):
    id             = models.UUIDField(default=uuid.uuid4, primary_key=True)
    category_name  = models.CharField(max_length=100, unique=True, null=True, blank=True)
    slug           = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    discription    = models.CharField(max_length=250, null=True, blank=True)
    cart_image     = models.ImageField(upload_to='images/categories', null=True, blank=True)
    
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        
    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return str(self.category_name)

    def get_absolute_url(self):
        return reverse('cart-details', kwargs={'pk':id})
