from django.urls import path
from . import views
from accounts import views as AccountViews
urlpatterns = [
    path('' , AccountViews.vendorDashboard , name="vendor"),
    path('vendor_profile/' , views.vendor_profile , name = 'vendor_profile'),
    path('menu_builder/' , views.menu_builder , name='menu_builder'),
    path('menu_builder/category/<int:pk>/' , views.food_item_byCategory ,name='food_item_byCategory'),
    path('menu_builder/category/add' , views.add_category , name= 'add_category'),
    path('menu_builder/category/edit/<int:pk>/' , views.edit_category , name= 'edit_category'),
    path('menu_builder/category/delete/<int:pk>/' , views.delete_category , name= 'delete_category'),
    path('menu_builder/food/add' , views.add_foodItem , name= 'add_foodItem'),
    path('menu_builder/food/edit/<int:pk>/' , views.edit_foodItem , name= 'edit_foodItem'),
    path('menu_builder/food/delete/<int:pk>/' , views.delete_foodItem , name= 'delete_foodItem'),


]