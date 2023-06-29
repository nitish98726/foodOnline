from django.shortcuts import render , redirect
from vendor.models import Vendor , OpeningHour
from django.http import HttpResponse , JsonResponse
from menu.models import FoodItem
from .models import Cart
from .context_processors import get_cart_counter , get_cart_amounts
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# Geodjango modules
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from datetime import date , datetime
from orders.forms import OrderForm
from django.shortcuts import get_object_or_404
from accounts.models import UserProfile


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
    openinghour = OpeningHour.objects.filter(vendor=vendor).order_by('day' , '-from_hour')
    today_date = date.today()
    today = today_date.isoweekday()
    today_opening_hours = OpeningHour.objects.filter(vendor=vendor , day = today)
    is_open = vendor.is_open()
        
    context = {
        'openinghour':openinghour,
        'vendor':vendor,
        'cartitems':cartitems,
        'today_opening_hours':today_opening_hours,
        'is_open':is_open,
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
                    return JsonResponse({'status':'Success' ,'message':'Increased The Cart Quantity' , 'cart_counter':get_cart_counter(request) , 'qty':checkcart.quantity ,'cart_amount':get_cart_amounts(request)})
                except:
                    checkcart = Cart.objects.create(user=request.user , fooditem=fooditem , quantity =1 )
                    return JsonResponse({'status':'Success' , 'message':'New Item Added to Cart' , 'cart_counter':get_cart_counter(request) , 'qty':checkcart.quantity , 'cart_amount':get_cart_amounts(request)})
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
                    return JsonResponse({'status':'Success'  , 'cart_counter':get_cart_counter(request) , 'qty':checkcart.quantity , 'cart_amount':get_cart_amounts(request)})
                except:
                    
                    return JsonResponse({'status':'Failed' , 'message':'You do not have this item in cart' })
            except:
                return JsonResponse({'status':'Failed' ,'message':'Food Item Does not exists'})
        else:
            return JsonResponse({'status':'Failed' ,'message':'Invalid request'})
        
    
    else:
        return JsonResponse({'status':'login_required' ,'message':'please login to continue'})
    
@login_required(login_url = 'login')
def cart(request):
    cartitems  = Cart.objects.filter(user=request.user).order_by('-created_at')
    context =  {
        'cartitems':cartitems,
    }
    return render(request ,'marketplace/cart.html' , context)

def delete_cartitem(request , cart_id):
    if request.user.is_authenticated:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                cart_item = Cart.objects.get(user = request.user , id = cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status':'Success' , 'message':"Cart Item deleted succesfully " , "cart_counter":get_cart_counter(request) ,'cart_amount':get_cart_amounts(request)})
            except:
               return JsonResponse({'status':'Failed' ,'message':'Cart Item Does not exists'})
        else:
            return JsonResponse({'status':'Failed' , 'message':"Invalid Request"  })

# Search functionality on home page
def search(request):
    if request.method=='GET':
        keyword= request.GET['keyword']
        address = request.GET['address']
        lat = request.GET['lat']
        long = request.GET['long']
        radius = request.GET['radius']
        # get vendor id that has the user desired fooditem
        vendor_byFoodItem = FoodItem.objects.filter(Q(food_title__icontains=keyword , is_available=True)|Q(description__icontains=keyword , is_available=True)).values_list('vendor_id' , flat=True)
        vendors = Vendor.objects.filter(Q(id__in=list(set(vendor_byFoodItem))) |Q(vendor_name__icontains =keyword , is_approved=True , user__is_active=True))       
        if lat and long and radius:
            pnt = GEOSGeometry('POINT(%s %s)' % (long , lat))
            vendors = Vendor.objects.filter(Q(id__in=list(set(vendor_byFoodItem))) |Q(vendor_name__icontains =keyword , is_approved=True , user__is_active=True) , 
                                            user_profile__location__distance_lte=(pnt , D(km=radius))
                                            ).annotate(distance=Distance("user_profile__location" , pnt)).order_by('distance')
            for v in vendors:
                v.kms = round(v.distance.km ,1 )
        vendor_count = vendors.count()
        
        context = {
            'vendors':vendors,
            'vendor_count':vendor_count,
            'source_location':address,
        }
    
    return render(request , 'marketplace/listings.html' ,context)
@login_required(login_url = 'login')
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    
    if cart_count==0:
        return redirect('marketplace')
    user_profile = get_object_or_404(UserProfile , user=request.user)
    defaut_values = {
        'first_name':request.user.first_name,
        'last_name':request.user.last_name,
        'phone':request.user.phone_number,
        'email':request.user.email,
        'address':user_profile.address,
        'country':user_profile.country,
        'state':user_profile.state,
        'city':user_profile.city,
        
    }
    form = OrderForm(initial=defaut_values)
    context = {
        'form':form,
        'cart_items':cart_items,
       
    
    }
    return render(request , 'marketplace/checkout.html' , context)