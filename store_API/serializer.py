from dataclasses import fields
from rest_framework import serializers


from store.models import Product


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
       model = Product
       fields = ['product_name', 'slug', 'price', 'description', 'stock', 'is_available']