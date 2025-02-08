from .models import Category,Product
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.db.models import Q


# Create your views here.
def auth(request):
    if request.method == 'POST':
        action= request.POST.get('action')
        if action=='register':
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
                return redirect('auth')
        else:
            username = request.POST.get('Username')
            password = request.POST.get('password')

            user=authenticate(request,username=username,password=password)
            
            if user is not None:
                login(request,user)
                return redirect("home")
            else:
                messages.info(request, 'NO USER FOUND')
                return redirect('auth')
            
    return render(request, 'auth.html') 
    

def logout_(request):#   _  due to same function names for views and authenticate module
    logout(request)
    return redirect('auth')

def home(request):
    return render(request,'home_page.html')

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