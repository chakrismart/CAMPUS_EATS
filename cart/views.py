from django.shortcuts import render, get_object_or_404,redirect
from django.http import JsonResponse
from home.models import Product  
from .cart import Cart  
from django.contrib import messages

def cart_summary(request):

    cart=Cart(request)
    products=cart.get_products()
    quantities=cart.get_quantities()
    total=cart.get_total()
    #print(total)
    return render(request,'cart.html',{'products':products,'quantities':quantities,'total':total})



def cart_add(request):
    cart = Cart(request)

    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))
        product_quantity=request.POST.get("product_qt")
        product = get_object_or_404(Product, id=product_id)
        #print(product.id,product.name)
        cart.add(product=product,quantity=product_quantity)
        #print(product.id,product.name)
        messages.info(request,"PRODUCT ADDED TO CART")
        return redirect('category')

    
    return JsonResponse({"error": "Invalid request"}, status=400)

def cart_update(request):
    cart=Cart(request)

    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))
        product_quantity=request.POST.get("product_qt")
    
        cart.update(product_id, product_quantity)

        return JsonResponse({"message": "Cart updated"})
    
def cart_delete(request):
    cart=Cart(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))
        #print('came to delete')
        cart.delete(product_id)

        return JsonResponse({"message": "item deleted"})

    

def cart_empty(request):
    cart=Cart(request)
    if request.POST.get("action") == "post":
        cart.empty()

        return JsonResponse({'message':'Cart emptied'})
