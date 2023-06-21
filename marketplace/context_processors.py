from .models import Cart
from menu.models import FoodItem

def get_cart_counter(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cartitems = Cart.objects.filter(user = request.user)
            if cartitems:
                for item in cartitems:
                    cart_count += item.quantity
            else:
                cart_count=0
        except:
            cart_count=0 

    return dict(cart_count=cart_count)

def get_cart_amounts(request):
    subtotal =0
    tax =0
    grand_total =0 
    if request.user.is_authenticated:
        cartitems = Cart.objects.filter(user = request.user)
        for item in cartitems:
            fooditem = FoodItem.objects.get(pk = item.fooditem.id)
            subtotal += (fooditem.price*item.quantity)

        grand_total = subtotal + tax
    return dict(subtotal=subtotal , grand_total=grand_total , tax=tax)