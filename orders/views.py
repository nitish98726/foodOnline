from django.shortcuts import render , redirect
from marketplace.models import Cart
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from marketplace.context_processors import get_cart_amounts
from .forms import OrderForm
from .models import Order , Payment , OrderFood
from datetime import datetime
from .utils import generate_order_number
from django.http import HttpResponse , JsonResponse
from accounts.utils import send_notification
import razorpay
from foodOnline.settings import RZP_KEY_ID , RZP_KEY_SECRET
from menu.models import FoodItem
from marketplace.models import Tax

# Create your views here.

client =  razorpay.Client(auth=(RZP_KEY_ID ,RZP_KEY_SECRET))

@login_required(login_url='login')
def place_order(request):
    cartitems = Cart.objects.filter(user = request.user).order_by('created_at')
    cartcount = cartitems.count()
    if cartcount<=0:
        return redirect('marketplace')
    vendor_ids = []
    for i in cartitems:
        if i.fooditem.vendor.id not in vendor_ids:
            vendor_ids.append(i.fooditem.vendor.id)
    # print(vendor_ids)
    # code piece for managing total per vendor
    get_tax = Tax.objects.filter(is_active=True)
    print(get_tax)
    subtotal =0
    k = {}
    for i in cartitems:
        fooditem = FoodItem.objects.get(pk=i.fooditem.id , vendor_id__in=vendor_ids)
        v_id = fooditem.vendor.id
        if v_id in k:
            subtotal = k[v_id]
            subtotal += (fooditem.price*i.quantity)
            k[v_id] = subtotal
        else:
            subtotal = (fooditem.price*i.quantity)
            k[v_id] = subtotal
    # print(k)
    tax_list = []
    for key in k.keys():
        
        for i in get_tax:
            # print(i)
            tax_type = i.tax_type
            tax_percentage = i.tax_percentage
            tax_amount = round((tax_percentage*k[key])/100 ,2)
            tax_dict = {
                key : {
                    k[key]:{
                    'tax_type': tax_type,
                    'tax_percentage': float(tax_percentage),
                    'tax_amount': float(tax_amount)
                    }
                }
            }
            tax_list.append(tax_dict)
         
    

    # subtotal = get_cart_amounts(request)['subtotal']
    total_tax = get_cart_amounts(request)['tax']
    grand_total = get_cart_amounts(request)['grand_total']
    tax_data = get_cart_amounts(request)['tax_list']
    if request.method =='POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order()
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.address  = form.cleaned_data['address']
            order.country = form.cleaned_data['country']
            order.city =  form.cleaned_data['city']
            order.pin_code = form.cleaned_data['pin_code']
            order.state = form.cleaned_data['state']
            order.tax_data = tax_data
            order.user = request.user
            order.total  = grand_total
            order.total_tax =total_tax
            order.payment_method = request.POST['payment_method']
            order.total_data =  tax_list
            order.save()
            order.order_number = generate_order_number(order.id)
            order.vendors.add(*vendor_ids)
            order.save()
            data = {
                "amount":float(order.total)*100,
                "currency": "INR",
                "receipt": "receipt #"+order.order_number 
                }
            payment = client.order.create(data=data)
            rzp_order_id = payment['id']
            # print(payment)
            context = {
               'order' :order,
               'cartitems':cartitems,
               'rzp_order_id':rzp_order_id,
               'RZP_KEY_ID':RZP_KEY_ID,
               'rzp_amount':data['amount']
            }
            return render(request , 'orders/place_order.html' , context)
        else:
            print(form.errors)
    return render(request , 'orders/place_order.html')

@login_required(login_url='login')
def payments(request):
    # check ajax request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method=="POST":
        # store in payment model
        order_number = request.POST['order_number']
        transaction_id = request.POST['transaction_id']
        payment_method = request.POST['payment_method']
        status = request.POST['status']
        razorpay_order_id = request.POST['razorpay_order_id']
        signature = request.POST['razorpay_signature']
        new_status = client.utility.verify_payment_signature({
        'razorpay_order_id': razorpay_order_id,
        'razorpay_payment_id': transaction_id,
        'razorpay_signature': signature
        })
        if new_status:
            order = Order.objects.get(user = request.user , order_number=order_number)
            payment = Payment.objects.create(user = request.user , transaction_id=transaction_id , payment_method=payment_method ,amount = order.total , status=status)
            payment.save()
            # Update Order Model
            order.payment = payment
            order.is_ordered = True
            order.save()
            # MOVE  CART ITEM TO ORDERED MODEL
            cartitems = Cart.objects.filter(user=request.user)
            for item in cartitems:
                orderedfood = OrderFood()
                orderedfood.order = order
                orderedfood.payment = payment
                orderedfood.user = request.user
                orderedfood.fooditem = item.fooditem
                orderedfood.quantity = item.quantity
                orderedfood.price = item.fooditem.price
                orderedfood.amount = item.fooditem.price *item.quantity
                orderedfood.save()
            
            # Send Order Confirmation mail
            mail_subject = 'Thanks for Ordering With us'
            mail_template = 'orders/order_confirmation_email.html'
            context = {
                'user':request.user,
                'order':order,
                'to_email':order.email,
            }
            send_notification(mail_subject , mail_template , context)
            # Send Order Received Mail to vendor or vendors
            mail_subject = 'You have received a new order'
            mail_template = 'orders/new_order_received.html'
            to_email = []
            for i in cartitems:
                if i.fooditem.vendor.user.email not in to_email:
                    to_email.append(i.fooditem.vendor.user.email)
            
            context = {
                'order':order,
                'to_email':to_email,
            }
            send_notification(mail_subject , mail_template , context)
            # Clear the cart 
            cartitems.delete()
            
            # Return json response to ajax request
            response = {
                'status':'Success',
                'message':'Payment has been properly handled',
                'order_number':order_number,
                'transaction_id':transaction_id,

            }
            return JsonResponse(response)
        else:
            return JsonResponse({
                'status':"Failed",
                'message':"Paymet Failed ! If your money has been deducted ,A refund will be inititated within 7 working days"
            })
                
           

        

    return HttpResponse("Payments View")
def order_complete(request):
    if request.method=="GET":
        order_number = request.GET['order_number']
        transaction_id = request.GET['transaction_id']
        try:
            order = Order.objects.get(order_number = order_number , payment__transaction_id=transaction_id , is_ordered=True)
            orderfood = OrderFood.objects.filter(order=order)
            subtotal =0
            for item in orderfood:
                subtotal += item.price*item.quantity
            context = {
                'order':order ,
                'orderfood':orderfood,
                'subtotal':subtotal,
            }
            return render(request , 'orders/order_complete.html' , context)
        except:
            return redirect('home')
    return render(request , 'orders/order_complete.html')