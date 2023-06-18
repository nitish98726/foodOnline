from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager
from django.db.models.signals import post_save , pre_save
from django.dispatch import receiver

class UserManager(BaseUserManager):
    def create_user(self , first_name , last_name , username , email , password=None):
        if not email:
            raise ValueError("User Must have an Email Address")
        if not username:
            raise ValueError('user must have Username')
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        user.set_password(password)
        user.save(using= self._db)
        return user
    def create_superuser(self , first_name , last_name , email, username ,password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        user.is_admin = True
        user.is_active =True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using= self._db)
        return user

# Create your models here.
class User(AbstractBaseUser):
    RESTAURANT = 1
    CUSTOMER = 2
    ROLE_CHOICES = (
        (RESTAURANT , "Restaurant"),
        (CUSTOMER , "Customer"),
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50 ,unique=True)
    email = models.EmailField(max_length=100 , unique=True)
    phone_number = models.CharField(max_length=50)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES , blank=True , null=True)

    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username' , 'first_name' , 'last_name']
    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self , perm , obj=None):
        return self.is_admin

    def has_module_perms(self , add_label):
        return True
    
    def get_role(self):
        if self.role == 1:
            user_role = 'Restaurant'
        elif self.role == 2:
            user_role = "Customer"
        
        return user_role


class UserProfile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    address = models.CharField(blank=True , max_length=250)
   
    profile_picture = models.ImageField(blank=True,upload_to='user/profile_pictures' )
    cover_picture = models.ImageField(blank=True,upload_to='user/cover_pictures' )
    city = models.CharField(blank=True , max_length=20)
    state = models.CharField(blank=True , max_length=20)
    country = models.CharField(blank=True , max_length=20 , default="INDIA")
    latitude = models.CharField(max_length=20 , blank=True)
    longitude = models.CharField(max_length=20 , blank = True)
    created_at =models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name
    
    

