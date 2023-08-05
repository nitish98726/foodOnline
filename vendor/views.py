from django.shortcuts import render
from django.http import HttpResponse , JsonResponse
from .forms import VendorForm , OpeningHourForm
from accounts.forms import UserProfileForm
from django.shortcuts import get_object_or_404
from accounts.models import UserProfile
from .models import Vendor , OpeningHour
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test ,login_required
from accounts.views import check_role_vendor
from menu.models import Category , FoodItem
from menu.forms import CategoryForm , FoodItemForm
from django.utils.text import slugify
from django.db import IntegrityError
from orders.models import Order , OrderFood

# Create your views here.

def register_vendor(request):
    return HttpResponse("Welcome to vendor registration page")
def get_vendor(request):
    vendor = Vendor.objects.get(user = request.user)
    return vendor


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendor_profile(request):
    profile = get_object_or_404(UserProfile , user = request.user )
    vendor = get_object_or_404(Vendor ,user = request.user)
   

    if request.method =="POST":
        profile_form = UserProfileForm(request.POST , request.FILES , instance=profile)
        vendor_form = VendorForm(request.POST , request.FILES , instance =vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request , "vendor Profile is updated")
            return redirect('vendor_profile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm( instance = vendor)
    context = {
        'profile_form':profile_form,
        'vendor_form':vendor_form,
        'profile':profile,
        'vendor':vendor,
    }

    return render(request , 'vendor/vendor_profile.html' , context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor =get_vendor(request)
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')

    context = {
        'categories':categories,
    }
    return render(request , 'vendor/menu_builder.html' , context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def food_item_byCategory(request ,  pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category , pk=pk)
    fooditems = FoodItem.objects.filter(vendor=vendor , category=category)
   
    context = {
        'fooditems':fooditems,
        'category':category,
    }
    return render(request , 'vendor/food_item_byCategory.html' , context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category_description = form.cleaned_data['description']
            vendor = get_vendor(request)
            
            category = Category.objects.create(category_name=category_name , vendor= vendor  , description = category_description)
            category.save()
            category.slug = slugify(category_name)+'-'+str(category.id)
            category.save()
            messages.success(request , "Category Added Succesfully")
            return redirect('menu_builder')
        else:
            print(form.errors)
    else:
        form = CategoryForm()
    
    context = {
        'form':form,
    }
    return render(request , 'vendor/add_category.html' , context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_category(request ,  pk=None):
    category = get_object_or_404(Category , pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST , instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            updated_category = form.save(commit=False)
            updated_category.vendor = get_vendor(request)
            updated_category.slug = slugify(category_name)
           
            updated_category.save()
            messages.success(request , "Category Updtaed Succesfully")
            return redirect('menu_builder')
        else:
            print(form.errors)
    else:
        form = CategoryForm(instance=category)
    
    context = {
        'form':form,
        'category':category
    }
    return render(request , 'vendor/edit_category.html' , context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_category(request , pk=None):
    category = get_object_or_404(Category , pk=pk)
    category.delete()
    messages.success(request , 'Category has been deleted successfully')
    return redirect('menu_builder')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_foodItem(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST , request.FILES)
        
        if form.is_valid():
            food_title = form.cleaned_data['food_title']
            food_category = form.cleaned_data['category']
            food_item = form.save(commit=False)
            food_item.vendor = get_vendor(request)
            food_item.is_available  = True
            
            food_item.slug = slugify(food_title)+'-'+str(food_item.id)
            food_item.save()
            fooditem = FoodItem.objects.get(food_title = food_title , vendor=get_vendor(request) , category = food_category)
            fooditem.slug = slugify(food_title)+'-'+str(food_item.id)
            fooditem.save()
            
            messages.success(request , "New Food Item Created Succesfully")
            return redirect('food_item_byCategory' , food_item.category.id)
        else:
            print(form.errors)
    else:
        form = FoodItemForm()
        form.fields['category'].queryset = Category.objects.filter(vendor = get_vendor(request))
    context = {
        'form': form,
    }

    return render(request , 'vendor/add_foodItem.html' ,  context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_foodItem(request , pk=None):
    food = get_object_or_404(FoodItem , pk=pk)
    if request.method == 'POST':
        form = FoodItemForm(request.POST , request.FILES, instance=food)
        
        if form.is_valid():
            food_title = form.cleaned_data['food_title']
            food_category = form.cleaned_data['category']
            food_item = form.save(commit=False)
            food_item.vendor = get_vendor(request)
            food_item.is_available  = True
            food_item.slug = slugify(food_title)
            
            food_item.save()
            fooditem = FoodItem.objects.get(food_title = food_title , vendor=get_vendor(request) , category = food_category)
            fooditem.slug = slugify(food_title)+'-'+str(food_item.id)
            fooditem.save()
            messages.success(request , "Food Item Updated Succesfully")
            return redirect('food_item_byCategory' , food_item.category.id)
        else:
            print(form.errors)
    else:
        form = FoodItemForm(instance=food)
        form.fields['category'].queryset = Category.objects.filter(vendor = get_vendor(request))
    context = {
        'form': form,
        'food':food,
    }
    return render(request , 'vendor/edit_foodItem.html' , context)

def delete_foodItem(request , pk=None):
    food = get_object_or_404(FoodItem , pk=pk)
    category = get_object_or_404(Category ,pk=food.category.id)
    food.delete()
    messages.success(request , 'Food Item has been deleted successfully')
    return redirect('food_item_byCategory' , category.id)

def opening_hours(request):
    opening_hours = OpeningHour.objects.filter(vendor = get_vendor(request))
    form = OpeningHourForm()
    context = {
        'form':form,
        'opening_hours':opening_hours,
    }
    return render(request , 'vendor/opening_hours.html' , context)

def add_opening_hours(request):
    if request.user.is_authenticated:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method=='POST':
            day = request.POST['day']
            from_hour = request.POST['from_hour']
            to_hour= request.POST['to_hour']
            is_closed = request.POST['is_closed']
            try:
                hour = OpeningHour.objects.create(vendor = get_vendor(request) , day = day , from_hour = from_hour , to_hour = to_hour ,is_closed = is_closed)
                if hour:
                    day = OpeningHour.objects.get(id = hour.id)
                    if day.is_closed:
                       response = {
                           'status':'success',
                           'id':hour.id,
                           'day':day.get_day_display(),
                           'is_closed':'Closed',
                        }
                    else:
                        response = {
                           'status':'success',
                           'id':hour.id,
                           'day':day.get_day_display(),
                           'from_hour':day.from_hour,
                           'to_hour':day.to_hour,
                           
                        }

                return JsonResponse(response)
            except IntegrityError as e:
               response = {
                   'status':'Failed',
                }
            return JsonResponse(response)
               
        else:
            return HttpResponse(" Not ET Voila!!")

def remove_opening_hours(request , pk):
    if request.user.is_authenticated:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            hour = OpeningHour.objects.get(pk= pk , vendor=get_vendor(request))
            hour.delete()
           
            print(pk)
            return JsonResponse({
                'status':"Success",
                'message':"Removed Opening Hour successfully",
                'id':pk,
            })
        else:
            return JsonResponse({
            'status':"Failed",
            'message':"Invalid request or problem fetching Hour Model",
            })
    else:
        return JsonResponse({
            'status':"Failed",
            'message':"You do not have permissions to do this",
            
        })
def order_detail(request , order_number):
    try:
        order = Order.objects.get(order_number=order_number , is_ordered=True)
        ordered_food = OrderFood.objects.filter(order=order , fooditem__vendor = get_vendor(request))
        # print(ordered_food)
        context = {
            'order':order,
            'ordered_food':ordered_food,
            'subtotal':order.get_total_by_vendor()['subtotal'],
            'tax_amount':order.get_total_by_vendor()['tax_amount'],
            'grand_total':order.get_total_by_vendor()['grand_total'],
        }
    except:
        return redirect('vendor')
    return render(request , 'vendor/order_detail.html',context)

def my_orders(request):
    vendor = Vendor.objects.get(user=request.user)
    orders = Order.objects.filter(vendors__in = [vendor.id] , is_ordered=True).order_by('created_at')
    context = {
        'orders':orders,
    }
    return render(request , 'vendor/my_orders.html' , context)