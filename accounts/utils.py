from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from .models import User

def detectUser(user):
    if user.role ==1:
        redirectUrl = 'vendorDashboard'
    elif user.role==2:
        redirectUrl = 'custDashboard'

        
    elif user.role ==None and user.is_superadmin:
        redirectUrl = '/admin'
    return redirectUrl

def send_verification_mail(request , user):
    current_site = get_current_site(request)
    main_subject = "Please activate your account"
    message = render_to_string("accounts/emails/account_verification.html" , {
        "user":user,
        'domain':current_site,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    send_email = EmailMessage(main_subject , message , to=[to_email])
    send_email.send()
def user_activation(request ,uidb64,token):
    try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User._default_manager.get(pk =uid)
    except(TypeError, ValueError,OverflowError,User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        user.is_active = True
        user.save()

def send_password_reset_mail(request ,  user):
    current_site = get_current_site(request)
    main_subject = "Reset Your Password"
    message = render_to_string("accounts/emails/reset_password_mail.html" , {
        "user":user,
        'domain':current_site,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    send_email = EmailMessage(main_subject , message , to=[to_email])
    send_email.send()

def send_notification(main_subject ,mail_template,context):
    
    
    message = render_to_string(mail_template,context)
    to_email = context['user'].email
    send_email = EmailMessage(main_subject , message , to=[to_email])
    send_email.send()