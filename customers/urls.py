from django.urls import path
from accounts import views as AccountViews
from . import views
urlpatterns = [
    path('' , AccountViews.custDashboard , name='customer'),
    path('customer_profile/' , views.customer_profile , name= 'customer_profile')
]