from django.contrib import admin
from .models import Order ,OrderFood ,Payment
# Register your models here.
class OrderFoodInline(admin.TabularInline):
    model = OrderFood
    extra =0
    readonly_fields = ['order' , 'payment' , 'user' , 'fooditem' , 'quantity' , 'price' , 'amount']
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user' , 'payment' , 'order_number' , 'email' , 'total' , 'total_tax' , 'status' , 'is_ordered']
    search_fields = ['user' , 'is_ordered']
    inlines = [OrderFoodInline]
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user' , 'transaction_id' , 'payment_method' , 'amount' , 'status']
    search_fields = ['user' , 'status']
class OrderFoodAdmin(admin.ModelAdmin):
    list_display = ['user' , 'payment' , 'user' , 'fooditem' , 'quantity' , 'price' , 'amount' ]
    search_fields = ['user' , 'order_number']




admin.site.register(Order , OrderAdmin)
admin.site.register(OrderFood , OrderFoodAdmin)
admin.site.register(Payment , PaymentAdmin)