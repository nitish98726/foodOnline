from django.shortcuts import render
from vendor.models import Vendor
from django.http import HttpResponse , JsonResponse
from menu.models import FoodItem
from .models import Cart
from .context_processors import get_cart_counter
# Create your views here.
def marketplace(request):
    vendors = Vendor.objects.filter(is_approved = True , user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors':vendors,
        'vendor_count':vendor_count,
    }
    return render(request , 'marketplace/listings.html' , context)

def vendor_detail(request , vendor_slug):
    vendor = Vendor.objects.get(vendor_slug = vendor_slug)
    
    if request.user.is_authenticated:
        cartitems = Cart.objects.filter(user = request.user)
    else:
        cartitems = None
    context = {
        'vendor':vendor,
        'cartitems':cartitems,
    }
    return render(request , 'marketplace/vendor_detail.html' , context)

def add_to_cart(request , food_id):
    if request.user.is_authenticated:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                fooditem = FoodItem.objects.get(id = food_id)
                try:
                    checkcart = Cart.objects.get(user = request.user , fooditem=fooditem)
                    # Increase cart Quantity
                    checkcart.quantity +=1
                    checkcart.save()
                    return JsonResponse({'status':'Success' ,'message':'Increased The Cart Quantity' , 'cart_counter':get_cart_counter(request) , 'qty':checkcart.quantity})
                except:
                    checkcart = Cart.objects.create(user=request.user , fooditem=fooditem , quantity =1 )
                    return JsonResponse({'status':'Success' , 'message':'New Item Added to Cart' , 'cart_counter':get_cart_counter(request) , 'qty':checkcart.quantity})
            except:
                return JsonResponse({'status':'Failed' ,'message':'Food Item Does not exists'})
        else:
            return JsonResponse({'status':'Failed' ,'message':'Invalid request'})
        
    
    else:
        return JsonResponse({'status':'login_required' ,'message':'Please Login to continue'})
    
def decrease_cart(request , food_id):
    if request.user.is_authenticated:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                fooditem = FoodItem.objects.get(id = food_id)
                try:
                    checkcart = Cart.objects.get(user = request.user , fooditem=fooditem)
                    # decrease cart Quantity
                    if checkcart.quantity >1:
                        checkcart.quantity -=1
                        checkcart.save()
                        
                    else:
                        checkcart.delete()
                        checkcart.quantity=0  
                    return JsonResponse({'status':'Success'  , 'cart_counter':get_cart_counter(request) , 'qty':checkcart.quantity})
                except:
                    
                    return JsonResponse({'status':'Failed' , 'message':'You do not have this item in cart' })
            except:
                return JsonResponse({'status':'Failed' ,'message':'Food Item Does not exists'})
        else:
            return JsonResponse({'status':'Failed' ,'message':'Invalid request'})
        
    
    else:
        return JsonResponse({'status':'login_required' ,'message':'please login to continue'})
    
def cart(request):
    return render(request ,'marketplace/cart.html')