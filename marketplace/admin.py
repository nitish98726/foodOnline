from django.contrib import admin

# Register your models here.
from .models import Cart

class CartAdmin(admin.ModelAdmin):
    list_display = ['user' , 'fooditem' , 'quantity' , 'created_at' , 'updated_at']

admin.site.register(Cart , CartAdmin)