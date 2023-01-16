from itertools import product
from tabnanny import verbose
import uuid

from django.db import models
from django.conf import settings
from django.urls import reverse
from django.db.models import Avg, Count

from account.models import CustomUser


from category.models import Cartegory

# Create your models here.

class Product(models.Model):
    product_name   = models.CharField(max_length=200, unique=True, null=True)
    slug           = models.SlugField(max_length=200, unique=True, null=True)
    price          = models.FloatField(default=0.0)
    description    = models.TextField(max_length=500, null=True)
    images         = models.ImageField(upload_to='images/products_img', default='')
    stock          = models.IntegerField(null=True, blank=True)
    is_available   = models.BooleanField(default=True, null=True, blank=True)
    category       = models.ForeignKey(Cartegory, on_delete=models.CASCADE, null=True)
    created_date   = models.DateTimeField(auto_now_add=True, null=True)
    modified_date  = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return self.product_name
    
    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg
    
    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('rating'))
        cnt = 0
        if reviews['count'] is not None:
            cnt = int(reviews['count'])
        return cnt
            
    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])


class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)


variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
) 


class Variation(models.Model):
    product             = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value     = models.CharField(max_length=100)
    is_active           = models.BooleanField(default=False)
    created_date        = models.DateTimeField(auto_now=True)
    
    objects = VariationManager()
    
    def __str__(self):
        return self.variation_value
    
    
    
class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.subject
        
    
class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)
    image = models.ImageField(upload_to='store/products', max_length=255)
    
    def __str__(self):
        return self.product.product_name
    
    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery'
    
    
    
    
    
    
