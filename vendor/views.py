from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def register_vendor(request):
    return HttpResponse("Welcome to vendor registration page")

def vendor_profile(request):
    return render(request , 'vendor/vendor_profile.html')