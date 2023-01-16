from dataclasses import field
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


from store.models import Product
from .serializer import ProductSerializer
from account_API.permissions import AdminOrReadOnly 

class ProductApiViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]