from django.db import models
from vendor.models import Vendor
# Create your models here.
class Category(models.Model):
    vendor = models.ForeignKey(Vendor , on_delete=models.CASCADE)
    category_name = models.CharField(max_length=50 )
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=250 , blank=True)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
    
    def clean(self):
        self.category_name = self.category_name.capitalize()

    def __str__(self):
        return self.category_name

class FoodItem(models.Model):
   vendor = models.ForeignKey(Vendor , on_delete=models.CASCADE)
   category = models.ForeignKey(Category , on_delete=models.CASCADE)
   food_title = models.CharField(max_length=100)
   slug = models.SlugField(max_length=150 , unique=True)
   description = models.TextField(max_length=250 ,blank=True)
   price = models.IntegerField()
   image = models.ImageField(upload_to='foodImages')
   is_available = models.BooleanField(default=True)
   created_at =models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now_add=True)

   def __str__(self):
       return self.food_title
