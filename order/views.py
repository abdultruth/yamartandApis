import datetime
import json


from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages


# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


from cart.models import CartItem
from .models import Order, OrderProduct, Payment
from store.models import Product


from .forms import OrderForm


def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])

    #Store transaction dsetails insider Payment model
    payment = Payment(user=request.user, 
                      payment_method=body['payment_method'],
                      payment_id = body['transID'],
                      amount_paid= order.order_total,
                      status=body['status'],
                    )
    payment.save()
    
    order.payment = payment
    order.is_ordered = True
    order.save()
    
    # Move the cart item to Order Product table
    cart_items = CartItem.objects.filter(user=request.user)
    
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.order = True
        orderproduct.save()
        
        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()
        
        
        # Reduce the quantity of the sold products
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()
        
    # Clear cart
    CartItem.objects.filter(user=request.user).delete()    
    
    # Send order received e-mail to customer
    current_site = get_current_site(request)
    mail_subject = 'Thank you for your order!'
    message = render_to_string('order/order_recieved_email.html', {
            'user': request.user,
            'order': order,
            
            })
            
    to_email = request.user.email      
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()
    
    # Send order number and transaction id back to sendData method via JsonResponse
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }
    
    # return render(request, 'order/payments.html', data)
    return JsonResponse(data)


def place_order(request, total=0, quantity=0):
    # if the cart count is less than or equal to 0, then re 
    cart_items = CartItem.objects.filter(user=request.user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = total + tax
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order()
            order.user = request.user
            order.first_name = request.POST['first_name']
            order.last_name = request.POST['last_name']
            order.phone = request.POST['phone']
            order.email = request.POST['email']
            order.address_line_1 = request.POST['address_line_1']             
            order.address_line_2 = request.POST['address_line_2']
            order.country = request.POST['country']
            order.state = request.POST['state']
            order.city = request.POST['city']
            order.order_note = request.POST['order_note']
            order.order_total = grand_total
            order.tax = tax
            order.ip = request.META.get('REMOTE_ADDR')
            order.save()
            
            # Generate order number
            yr = int(datetime.date.today().strftime('%y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date= d.strftime("%Y%m%d")
            order_number = current_date + str(order.id)
            order.order_number = order_number
            order.save()
            
            myorder = Order.objects.get(user=request.user, is_ordered=False, order_number=order_number)
            
            context = {
                'order': myorder,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }
            return render(request, 'order/payments.html', context)
        else:
            pass        
    return render(request, 'store/place-order.html')

def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('TransID')
    
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        
        subtotal = 0
        for i in ordered_products:
            subtotal +=  i.product_price * i.quantity
        
        
        payment = Payment.objects.get(payment_id=transID)
        
        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order_number,
            'transID': order.payment.id,
            'payment': payment,
            'subtotal': subtotal,
        }
        return render(request,'order/order_complete.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')
    
   


    
