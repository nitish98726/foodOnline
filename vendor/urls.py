from django.urls import path
from . import views
from accounts import views as AccountViews
urlpatterns = [
    path('' , AccountViews.vendorDashboard , name="vendor"),
    path('vendor_profile/' , views.vendor_profile , name = 'vendor_profile'),
]