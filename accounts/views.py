from django.shortcuts import render , redirect
from django.http import HttpResponse
from .forms import UserForm
from .models import User
from django.contrib import messages
# Create your views here.

def registerUser(request):
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
    return HttpResponse('This is Login Page')