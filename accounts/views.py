from django.shortcuts import render , redirect
from django.http import HttpResponse
from .forms import UserForm
from .models import User , UserProfile
from django.contrib import messages
from vendor.forms import VendorForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required , user_passes_test
from .utils import detectUser
from django.core.exceptions import PermissionDenied
# Create your views here.

def check_role_vendor(user):
    if user.role==1:
        return True
    else:
        raise PermissionDenied
def check_role_customer(user):
    if user.role==2:
        return True
    else:
        raise PermissionDenied

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request , "You are already a Registered User ")
        return redirect('myAccount')
    if request.method =='POST':
        print(request.POST)
        form = UserForm(request.POST)
        if form.is_valid():
          first_name = form.cleaned_data['first_name']
          last_name = form.cleaned_data['last_name']
          
          email = form.cleaned_data['email']
          password = form.cleaned_data['password']
          username = form.cleaned_data['username']
          user = User.objects.create_user(first_name = first_name ,last_name=last_name , email = email , username =username , password=password)
          user.role = User.CUSTOMER
          messages.info(request , "Your account has been registered successfully")    
          user.save()  
        else:
             print(form.errors)
           
            
    else:    
         form = UserForm()
    
    context = {
         'form':form,
     }
    return render(request , 'accounts/registerUser.html' , context)

def login(request):
    if request.user.is_authenticated:
        messages.warning(request , "You are already Logged In ")
        return redirect('myAccount')
    if request.method =="POST":
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email =email , password=password)
        if user is not None:
            auth.login(request , user)
            messages.success(request , "You are Logged in")
            return redirect('myAccount')
        else:
            messages.error(request , 'Login Credentials Donot Match')
            return redirect('login')


    return render(request , 'accounts/login.html')
def logout(request):
    auth.logout(request)
    messages.info(request,'You are Logged Out')
    return redirect('login')


def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request , "You are already a Registered User ")
        return redirect('myAccount')
    if request.method =='POST':
        form = UserForm(request.POST)
        vendor_form = VendorForm(request.POST , request.FILES)
        if form.is_valid() and vendor_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = form.cleaned_data['username']
            user = User.objects.create_user(first_name = first_name ,last_name=last_name , email = email , username =username , password=password)
            user.role = User.RESTAURANT
            user.save()
            vendor = vendor_form.save(commit = False)
            vendor.user = user
            user_profile =  UserProfile.objects.get(user=user)
            vendor.user_profile =  user_profile
            
            vendor.save()
            messages.info(request , "Your account has been registered successfully")
            
        else:
            print(form.errors)

    else:
        form = UserForm()
        vendor_form = VendorForm()
    
    context = {
        'form':form,
        'vendor_form':vendor_form,

    }
    return render(request , 'accounts/registerVendor.html' , context)

@login_required(login_url='/accounts/login')
def myAccount(request):
    user = request.user
    redirectUrl= detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url='/accounts/login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request , 'accounts/custDashboard.html')

@login_required(login_url='/accounts/login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request , 'accounts/vendorDashboard.html')