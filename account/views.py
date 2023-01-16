
import re
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.contrib import auth, messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from account.models import CustomUser, UserProfile
from cart.models import Cart, CartItem


from cart.views import _get_cart_id
from order.models import Order


from .forms import RegistrationForm, UserForm ,UserProfileForm

# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.
@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST) # 'request.POST' will contain all the request value
        print(form.errors)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_no = form.cleaned_data['phone_no']
            
            user = CustomUser.objects.create_user(first_name=first_name, last_name=last_name, email=email, phone_no=phone_no)
            user.save()
           
            
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_activation_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            
            messages.success(request, 'Registration successful!!!')
            return redirect('store')
    else:
        form = RegistrationForm()
        
    context = {
                'form': form,
            }
    return render(request, 'accounts/register.html', context)


def login(request):    
    if request.method =='POST':
       email = request.POST['email']
       password = request.POST['password']
    
       user = auth.authenticate(request, email=email, password=password)
       
       if user is not None:
           auth.login(request, user)
           try:
               cart = Cart.objects.get(cart_id=_get_cart_id(request))
               is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
    
               if is_cart_item_exists:
                   cart_item = CartItem.objects.filter(cart=cart)
               # getting the product variation by cart id     
                   product_variation = []
                   for item in cart_item:
                       variation = item.variations.all()
                       product_variation.append(list(variation))
                       
                   cart_item = CartItem.object.filter(user=user)
                   ex_var_list = []
                   id = []
                   for item in cart_item:
                       existing_variation = item.variations.all()
                       ex_var_list.append(list(existing_variation))
                       id.append(item.id)
                   
                # product_variation = [1,2,3,4,6]
                # ex_var_list = [4,6,3,5]
                
                   for pr in product_variation:
                       if pr in ex_var_list:
                          index = ex_var_list.index(pr)
                          item_id = id[index]
                          item = CartItem.objects.get(id=item_id)
                          item.quantity += 1
                          item.user = user
                          item.save()
                       else:
                          cart_item = CartItem.objects.filter(cart=cart) 
                          for item in cart_item:
                              item.user = user
                              item.save()
           except:
              auth.login(request, user) 
              messages.success(request, 'You are now logged in!')
              return redirect('accounts:dashboard')
    
    return render(request, 'accounts/login.html')


@login_required(login_url = 'accounts:login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'you are logged out.')
    return redirect('accounts:login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratutions! Your Account has been activated.')
        return redirect('accounts:login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('accounts:register')
    
 

@login_required(login_url = 'accounts:login')
def dashboard(request):
    userprofile = get_object_or_404(UserProfile, user= request.user)
    order = Order.objects.order_by('created_at').filter(user_id=request.user.id, is_ordered=True)
    order_count = order.count()
    if order:
        order = order
    else:
        order = None
        
    context = {
        'order': order,
        'order_count': order_count,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/dashboard.html', context)


def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email__iexact=email)
            
            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            
            messages.success(request, 'Password reset email has been sent to your email address')
            return redirect('login')
            
        else: 
            messages.error(request, 'Account does not exist')
            return redirect('accounts:forgotPassword')
            
    return render(request, 'accounts/forgetpassword.html')



def resetpassword_validate(request, uidb64, token):
    try: 
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please Reset your Password.')
        return redirect('accounts:resetPassword')
    else:
        messages.error(request, 'This link has expired.')
        return redirect('accounts:login')
    
    
def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
    
        if password == confirm_password:
            uid = request.session.get('uid')
            user = CustomUser.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password Reset successfully!')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Password mismatched!')
            return redirect('accounts:resetPassword')
    else:
        return render(request,'accounts/resetPassword.html')
    
    
    
@login_required(login_url = 'accounts:login')
def my_orders(request):
    orders = Order.objects.order_by('created_at').filter(user_id=request.user.id, is_ordered=True)
    
    context = {
        'orders': orders,
    }
    return render(request, 'accounts/my_orders.html', context)



@login_required(login_url = 'accounts:login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated')
            return redirect('accounts:edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
        
    context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'userprofile': userprofile,
        }
        
    return render(request, 'accounts/edit_profile.html', context)

@login_required(login_url = 'accounts:login')
def change_password(request):
    if request.method == "POST":
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_new_password = request.POST['confirm_new_password']
        
        user = auth.authenticate(email=request.user.email, password=current_password)
        
        if user != None:
            if new_password == confirm_new_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password Updated Successfully.')
            elif new_password != confirm_new_password:
                messages.error(request, 'Confirm password does not match!!!')
        else:
            messages.error(request, 'Please enter your valid current password')
    
    return render(request, 'accounts/change_password.html')