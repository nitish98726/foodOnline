from django.urls import path
from .import views

urlpatterns = [
    path('registerUser/' , views.registerUser ,name = 'registerUser'),
    path('login/' , views.login , name = 'login'),
    path('logout' , views.logout , name = 'logout'),
    path('custDashboard/' , views.custDashboard , name = 'custDashboard'),
    path('myAccount/' , views.myAccount , name = 'myAccount'),
    path('registerVendor' , views.registerVendor , name = 'registerVendor'),
    path('vendorDashboard/' , views.vendorDashboard , name = 'vendorDashboard'),
]