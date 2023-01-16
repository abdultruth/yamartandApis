from django.contrib import admin
from .models import Order, Payment, OrderProduct


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    # readonly_fields = ('payment', 'user', 'product', 'quatity', 'product_price', 'ordered')
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ['order_number','user', 'payment', 'full_name', 'city', 'email', 'order_total', 'tax', 'status', 'is_ordered', 'created_at']
    list_filter = ['status','is_ordered']
    search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'email']
    list_per_page = 20
    

class PaymentAdmin(admin.ModelAdmin):
    model = Payment
    list_display = ['user', 'payment_id', 'amount_paid', 'status', 'created_at']
    
    
class OrderProductAdmin(admin.ModelAdmin):
    model = OrderProduct
    list_display = ['order', 'payment', 'user', 'product']
    # inlines = [OrderProductInline]
    
    
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)