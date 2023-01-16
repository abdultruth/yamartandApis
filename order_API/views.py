from rest_framework import viewsets


from account_API.permissions import OrderMakerOrReadOnly


from order.models import Order, OrderProduct
from .serializer import OrderSerializer

class OrderApiViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [OrderMakerOrReadOnly]
    