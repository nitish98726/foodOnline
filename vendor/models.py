from django.db import models
from accounts.models import User ,  UserProfile
from accounts.utils import send_notification
from datetime import datetime , date 
from .utils import list_of_time

# Create your models here.
class Vendor(models.Model):
    user = models.OneToOneField(User , related_name='user' , on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile ,related_name='userprofile' , on_delete=models.CASCADE)
    vendor_slug = models.SlugField(max_length=150 , unique=True)
    vendor_name = models.CharField(max_length=100)
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name
    def save(self , *args,**kwargs):
        if self.pk is not None:
            
            orig = Vendor.objects.get(pk= self.pk)
            mail_template = 'accounts/emails/admin_vendorApproval_email.html'
            context = {
                'user':self.user,
                'is_approved':self.is_approved
            }
            if orig.is_approved != self.is_approved:
                if self.is_approved == True:
                    mail_subject = 'Your Restaurant has been approved!!'
                    
                    send_notification(mail_subject , mail_template , context)
                else:
                    mail_subject = 'Your Restaurant is not eligible.'
                    send_notification(mail_subject , mail_template , context)
        return super(Vendor,self).save(*args ,**kwargs)
    
    def is_open(self):
        today_date = date.today()
        today = today_date.isoweekday()
        today_opening_hours = OpeningHour.objects.filter(vendor=self , day = today)
        now = datetime.now()
        current_time  = now.strftime('%H:%M:%S')
        is_open = False
        for i in today_opening_hours:
            start = str(datetime.strptime(i.from_hour , "%I:%M %p").time())
            end = str(datetime.strptime(i.to_hour , "%I:%M %p").time())
            # print(start , end)
       
            if current_time > start and current_time < end:
                is_open = True
            
            else:
                is_open = False
        return is_open

class OpeningHour(models.Model):
    DAYS=[
        (1,('Monday')),
        (2,('Tuesday')),
        (3,('Wednesday')),
        (4,('Thursday')),
        (5,('Friday')),
        (6,('Saturday')),
        (7,('Sunday')),
    ]
    HOUR_OF_DAY_24 = list_of_time()
    vendor = models.ForeignKey(Vendor , on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS)
    from_hour = models.CharField(choices=HOUR_OF_DAY_24 , max_length=10 , blank=True)
    to_hour = models.CharField(choices=HOUR_OF_DAY_24 , max_length=10 , blank=True)
    is_closed = models.BooleanField(default=False)

    class Meta:
        ordering = ('day' , 'from_hour')
        unique_together = ('vendor' ,'day' , 'from_hour' , 'to_hour')
    
    def __str__(self):
        return self.get_day_display()