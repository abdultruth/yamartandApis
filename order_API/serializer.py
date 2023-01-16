from xml.etree.ElementInclude import include
from rest_framework import serializers


from order.models import Order, OrderProduct


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    len_first_name = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = ['user', 'len_first_name', 'order_number', 'first_name', 'last_name', 'phone', 'email','state', 'city', 'tax', 'order_total', 'is_ordered', 'ip', 'country', 'address_line_1']

            
    def get_len_first_name(self, object):
        return len(object.first_name)  
              