from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from accounts.forms import UserProfileForm , UserInfoForm
# Create your views here.
from accounts.models import UserProfile , User
from django.shortcuts import get_object_or_404
from django.contrib import messages

@login_required(login_url = 'login')

def customer_profile(request):
    profile  = get_object_or_404(UserProfile ,user=request.user)
    if request.method =="POST":
        profile_form = UserProfileForm(request.POST  , request.FILES , instance = profile)
        user_form = UserInfoForm(request.POST , instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request , "Profile updated Successfully")
            return redirect('customer_profile')
        else:
            print(profile_form.errors)
            print(user_form.errors)
    else:
        # user = get_object_or_404(User , email = request.user)
        profile_form = UserProfileForm(instance = profile)
        user_form = UserInfoForm(instance=request.user)
    
    context = {
        'profile_form':profile_form,
        'user_form':user_form,
        'profile':profile,
    }
    return render(request , 'customer/customer_profile.html' ,context)