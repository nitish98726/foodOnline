from django.db import models
from accounts.models import User
from menu.models import FoodItem
from vendor.models import Vendor
import json
# Create your models here.

request_object = ''

class Payment(models.Model):
    PAYMENT_METHOD = (
        ('PAYPAL','PAYPAL'),
        ('RAZORPAY' , 'RAZORPAY')
)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    payment_method =models.CharField(max_length=100 ,choices=PAYMENT_METHOD)
    amount = models.CharField(max_length=10)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_id
    
class Order(models.Model):
    STATUS = (
        ('NEW','NEW'),
        ('ACCEPTED' , 'ACCEPTED'),
        ('COMPLETED' , 'COMPLETED'),
        ('CANCELLED' , 'CANCELLED'),

    )
    user = models.ForeignKey(User , on_delete=models.SET_NULL , null=True)
    payment = models.ForeignKey(Payment , on_delete=models.SET_NULL ,blank=True , null=True)
    vendors = models.ManyToManyField(Vendor , blank=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15 , blank=True)
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=200)
    country = models.CharField(max_length=15 , blank=True)
    state = models.CharField(max_length=15 , blank=True)
    city = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=10)
    total = models.FloatField()
    tax_data = models.JSONField(blank=True , help_text="Data Format:{'tax_type':{'tax_percentage':'tax_amount'}}" , null=True)
    total_data = models.JSONField(blank=True , null=True)
    total_tax = models.FloatField()
    payment_method = models.CharField(max_length=25)
    status = models.CharField(max_length=15 , choices=STATUS , default='NEW')
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now =True)

    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'
    
    def __str__(self):
        return self.order_number
    def order_placed_to(self):
        return ", ".join([str(i) for i in self.vendors.all()])
    def get_total_by_vendor(self):
        vendor = Vendor.objects.get(user=request_object.user)
        if self.total_data:
            total_data = self.total_data
            sub_list = []
            for item in total_data:
                for key in item.keys():
                    # print(vendor.id)
                    # print(key)
                    if key == str(vendor.id):
                        sub_list.append(item[key])
            
            
            tax_amount=0
            for item1 in sub_list:
                for key2 , val in item1.items():
                    subtotal = float(key2)
                    tax_type = val['tax_type']
                    tax_amount += val['tax_amount']
                    tax_percentage = val['tax_percentage']
                    # print(tax_type , tax_amount , tax_percentage)
            grand_total = float(subtotal) + float(tax_amount)
            # print(subtotal , grand_total , tax_amount)
        return {
            'grand_total':grand_total , 
            'subtotal':subtotal,
            'tax_amount':tax_amount,
        }

class OrderFood(models.Model):
    order = models.ForeignKey(Order , on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment , on_delete=models.CASCADE)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    fooditem = models.ForeignKey(FoodItem , on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    def __str__(self):
        return self.fooditem.food_title