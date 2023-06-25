from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.forms import UserProfileForm , UserInfoForm
# Create your views here.
from accounts.models import UserProfile , User
from django.shortcuts import get_object_or_404
@login_required(login_url = 'login')

def customer_profile(request):
    profile  = get_object_or_404(UserProfile ,user=request.user)
    # user = get_object_or_404(User , email = request.user)
    profile_form = UserProfileForm(instance = profile)
    user_form = UserInfoForm(instance=request.user)
    context = {
        'profile_form':profile_form,
        'user_form':user_form,
    }
    return render(request , 'customer/customer_profile.html' ,context)