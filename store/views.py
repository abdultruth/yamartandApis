
from email import message
from itertools import product
from unicodedata import category
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.contrib import messages


from cart.models import CartItem
from order.models import OrderProduct 
from .models import Product, ProductGallery, ReviewRating
from category.models import Cartegory

from .forms import ReviewForm

from cart.views import _get_cart_id


def store(request, category_slug=None):
    categories = None
    products = None
    
    if category_slug != None:
        categories = get_object_or_404(Cartegory, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True).order_by('-created_date')
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        page_products = paginator.get_page(page)
        productscount = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('-created_date')
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        page_products = paginator.get_page(page)
        productscount = products.count()
        
    context = {
        'products': page_products,
        'productscount': productscount,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_get_cart_id(request), product=single_product).exists()
    except Exception as e :
        raise e
    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None
        
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)

    #get the product gallery 
    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)
    context = {
        'single_product':single_product,
        'in_cart':in_cart,
        'orderproduct': orderproduct,
        'reviews': reviews,
        'product_gallery': product_gallery,
    }
    return render(request, "store/product-detail.html", context)

 
def search(request, products=None):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
           products = Product.objects.filter(Q(product_name__icontains=keyword) | Q(description__icontains=keyword) )
           productscount = products.count()
           print(productscount)
        context = {
            'products':products,
            'productscount':productscount,
        }
    return render(request, 'store/store.html', context)


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    product = Product.objects.get(id=product_id)
    if request.method == "POST":
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            print(form)
            if form.is_valid():
                reviews = ReviewRating()
                reviews.subject = form.cleaned_data['subject']
                reviews.review = form.cleaned_data['review']
                reviews.rating = form.cleaned_data['rating']
                reviews.ip = request.META.get('REMOTE_ADDR')
                reviews.user = request.user
                reviews.product = product
                reviews.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
            return redirect(url)
    