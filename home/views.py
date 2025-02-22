from .models import Category,Product,Customer,Orders
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import json
from cart.cart import Cart
import json
import uuid
from django.utils.timezone import localtime
import pytz
# import gspread
# from google.oauth2.service_account import Credentials
# from django.conf import settings

def auth(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'register':
            username = request.POST.get('Username')
            email = request.POST.get('email')
            password = request.POST.get('password')

            if User.objects.filter(username=username).exists():
                messages.info(request, 'USERNAME TAKEN')
                return redirect('auth')

            elif User.objects.filter(email=email).exists():
                messages.info(request, 'EMAIL TAKEN')
                return redirect('auth')

            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                customer = Customer.objects.create(username=username, email=email)
                customer.save()

                request.session['username'] = username  # Store username in session
                return redirect('auth')  # Redirect to login after registration

        else:  # Login
            username = request.POST.get('Username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                
                current_user=Customer.objects.get(username=username)
                saved_cart=current_user.old_cart
                if saved_cart:
                    converted_cart=json.loads(saved_cart)
                    cart=Cart(request)
                    for key,value in converted_cart.items():
                        cart.db_add(key,value)
                
                
                request.session['username'] = username  # Store username in session
                # Check if user has updated profile
                try:
                    customer = Customer.objects.get(username=username)
                    if not customer.profile_updated:
                        return redirect("profile_update")  # Redirect to profile update
                except Customer.DoesNotExist:
                    return redirect("profile_update")  # Ensure profile exists

                return redirect("home")  # Normal login
            else:
                messages.info(request, 'NO USER FOUND')
                return redirect('auth')

    return render(request, 'auth.html')

def home(request):
    return render(request,'home_page.html')
    


def logout_(request):#   _  due to same function names for views and authenticate module
    logout(request)
    return redirect('auth')

def about(request):
   
    return render(request,'about.html')


def category(request,foo):
    foo=foo.replace('-',' ')
    category=Category.objects.get(name=foo)
   
    products=Product.objects.filter(category=category)
    
    return render(request,'category.html',{'products':products,'category':category})

def search(request):
    if request.method=='POST':
        item=request.POST.get('search')
       
        products=Product.objects.filter(Q(name__icontains=item)|Q(category__name__icontains=item))
        if not item:  # Ensure the search query is not empty
            return render(request, 'home_page.html')
        
        elif not products:
            return render(request, 'home_page.html')
        else:
            
            return render(request,'search.html',{'products':products}) 
    return render(request,'search.html')

def profile_update(request):
    username = request.session.get('username', '')

    if not username:
        return redirect('auth')  # Redirect to login if no session is found

    # Fetch customer data if it exists
    customer = Customer.objects.filter(username=username).first()

    return render(request, "profile_update.html", {"username": username, "customer": customer})


def save_profile(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        branch = request.POST.get('branch')
        regno = request.POST.get('regno')

        # Fetch customer by username
        customer = get_object_or_404(Customer, username=username)
        
        # Update fields only if they are provided
        customer.first_name = first_name if first_name else customer.first_name
        customer.last_name = last_name if last_name else customer.last_name
        customer.phone = phone if phone else customer.phone
        customer.branch = branch if branch else customer.branch
        customer.registered_no = regno if regno else customer.registered_no

        customer.profile_updated = True  # Ensure the profile is marked as updated
        customer.save()

        return redirect('home')  # Redirect to home after updating

    return render(request, 'profile_update.html')


def profile(request):
    customer = Customer.objects.get(username=request.user.username)
    return render(request, 'user_profile.html', {'customer': customer})



def checkout(request):
    cart=Cart(request)
    final_cart=cart.cart_checkout()
    total=cart.get_total()
    return render(request, "checkout.html", {"final_cart":final_cart, "total": total})


def place_order(request):
    if request.method == "POST":
        tid = request.POST.get("transaction_id")
        cart = request.POST.get("final_cart", {})
        total = request.POST.get("total")
        items=''
        for i in cart:
            if i not in ["'", '"', "{", "}"]:
                items+=i
                #print(i,items)

        #print(type(cart),items)
        order = Orders.objects.create(
            order_id=str(uuid.uuid4())[:8],  # Generate unique order ID
            transaction_id=tid,
            customer_name=request.user.username,  # Get logged-in username
            total_amount=total,
            items=items,
            status="Pending",
        )

       # add_order_to_sheets(order)

        return redirect("history")

# def add_order_to_sheets(order):
#     scopes = [
#         "https://www.googleapis.com/auth/spreadsheets",  #
#         "https://www.googleapis.com/auth/drive"  
#     ]

    
#     creds = Credentials.from_service_account_file(settings.GOOGLE_SHEETS_CREDENTIALS, scopes=scopes)

    
#     client = gspread.authorize(creds)
#     sheet = client.open("CANTEEN PAYMENTS").sheet1  

    
#     sheet.append_row([
#         order.order_id,
#         order.transaction_id,
#         order.customer_name,
#         order.items,        
#         order.total_amount,
#         order.status
#     ])
    

def history(request):
     # Ensure you use the India timezone
    last_10_orders = Orders.objects.order_by("-created_at")[:10]

    # Convert order timestamps to IST
    for order in last_10_orders:
        print(order.created_at)
        
        
    

    return render(request, "history.html", {
        "last_10_orders": last_10_orders
    })


