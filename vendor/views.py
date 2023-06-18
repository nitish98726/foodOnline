from django.shortcuts import render
from django.http import HttpResponse
from .forms import VendorForm
from accounts.forms import UserProfileForm
from django.shortcuts import get_object_or_404
from accounts.models import UserProfile
from .models import Vendor 
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test ,login_required
from accounts.views import check_role_vendor
from menu.models import Category , FoodItem
from menu.forms import CategoryForm , FoodItemForm
from django.utils.text import slugify
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

def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category_description = form.cleaned_data['description']
            vendor = get_vendor(request)
            slug = slugify(category_name)
            category = Category.objects.create(category_name=category_name , vendor= vendor , slug = slug , description = category_description)
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

def delete_category(request , pk=None):
    category = get_object_or_404(Category , pk=pk)
    category.delete()
    messages.success(request , 'Category has been deleted successfully')
    return redirect('menu_builder')

def add_foodItem(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST)
        
        if form.is_valid():
            food_title = form.cleaned_data['food_title']
            
            food_item = form.save(commit=False)
            food_item.vendor = get_vendor(request)
            food_item.is_available  = True
            food_item.slug = slugify(food_title)
            
            food_item.save()
            messages.success(request , "New Food Item Created Succesfully")
            return redirect('menu_builder')
        else:
            print(form.errors)
    else:
        form = FoodItemForm()
    context = {
        'form': form,
    }

    return render(request , 'vendor/add_foodItem.html' ,  context)

def edit_foodItem(request):
    return render(request , 'vendor/edit_foodItem.html')

def delete_foodItem(request):
    return HttpResponse('deleted')