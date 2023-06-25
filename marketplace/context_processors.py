from .models import Cart , Tax
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
    get_tax = Tax.objects.filter(is_active=True)
    tax_list = []
    
    tax=0
    grand_total =0 
    if request.user.is_authenticated:
        cartitems = Cart.objects.filter(user = request.user)
        for item in cartitems:
            fooditem = FoodItem.objects.get(pk = item.fooditem.id)
            subtotal += (fooditem.price*item.quantity)
        for i in get_tax:
            tax_type = i.tax_type
            tax_percentage = i.tax_percentage
            tax_amount = round((tax_percentage*subtotal)/100 ,2)
            tax_dict = {
                'tax_type': tax_type,
                'tax_percentage': float(tax_percentage),
                'tax_amount': float(tax_amount)
            }
            tax_list.append(tax_dict)
            
        # print(tax_list)
        
        for tax_dict in tax_list:
            tax += tax_dict['tax_amount']

       
        grand_total = subtotal + tax
    return {
        'subtotal': subtotal,
        'grand_total': grand_total,
        'tax': tax,
        'tax_list': tax_list
    }
