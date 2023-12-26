import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from PIL import Image
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField
from django.core.validators import RegexValidator
from django.urls import reverse


from django.db.models import Q
from datetime import timedelta

import zoneinfo

from timezone_field import TimeZoneField


from .manager import CustomUserManager


class LowercaseEmailField(models.EmailField):
    """
    Override EmailField to convert emails to lowercase before saving.
    """
    def to_python(self, value):
        """
        Convert email to lowercase.
        """
        value = super(LowercaseEmailField, self).to_python(value)
        # Value can be None so check that it's a string before lowercasing.
        if isinstance(value, str):
            return value.lower()
        return value

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = LowercaseEmailField(_('email address'), unique=True)
    #username = models.CharField(max_length=50, unique=True)
    name = models.CharField(null=True, blank=True, max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    
    class Types(models.TextChoices):
        ORGANIZER = "Organizer", "ORGANIZER"
        AUDIENCE = "Audience", "AUDIENCE"
        

    default_type = Types.AUDIENCE

    type = MultiSelectField(choices=Types.choices, default=[], null=True, blank=True, max_length=9)
    

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.id}: {self.email}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.type.append(self.default_type)
        return super().save(*args, **kwargs)


class AudienceAdditional(models.Model):
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    profile_picture = models.ImageField(default='default.jpg', upload_to='profile_pics')


class OrganizerAdditional(models.Model):
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    website_url = models.URLField(max_length=200, blank=True)
    profile_picture = models.ImageField(default='default.jpg', upload_to='profile_pics')
    timezone = TimeZoneField(choices_display="WITH_GMT_OFFSET", default='Asia/Kathmandu')
    phone_regex = RegexValidator( regex = r'^\d{10}$',message = "phone number should exactly be in 10 digits")
    phone = models.CharField(max_length=255, validators=[phone_regex], blank = True, null=True) 

    

    
# Model Managers for proxy models
class OrganizerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        #return super().get_queryset(*args, **kwargs).filter(type = CustomUser.Types.SELLER)
        return super().get_queryset(*args, **kwargs).filter(Q(type__contains = CustomUser.Types.ORGANIZER))

class AudienceManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        #return super().get_queryset(*args, **kwargs).filter(type = CustomUser.Types.CUSTOMER)
        return super().get_queryset(*args, **kwargs).filter(Q(type__contains = CustomUser.Types.AUDIENCE))
       


# Proxy Models. They do not create a seperate table
class Organizer(CustomUser):
    default_type = CustomUser.Types.ORGANIZER
    objects = OrganizerManager()
    class Meta:
        proxy = True
    
    def sell(self):
        print("I can sell")

    @property
    def showAdditional(self):
        return self.selleradditional

class Audience(CustomUser):
    default_type = CustomUser.Types.AUDIENCE
    objects = AudienceManager()
    class Meta:
        proxy = True 

    def buy(self):
        print("I can buy")

    @property
    def showAdditional(self):
        return self.customeradditional

class Category(models.Model):
    cat_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150,db_index=True)
    
    def __str__(self):
        return self.name
    

class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150)
    event_description = models.TextField(max_length=500, blank=True)  
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    start_time = models.TimeField(default=timezone.now)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    venue = models.CharField(max_length=150)
    capacity = models.IntegerField()
    image = models.ImageField(default="default_banner.png", upload_to="event_images")
    price = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
	     return self.title
   



class CartManager(models.Manager):
    def create_cart(self, user):
        cart = self.create(user = user)
        return cart

class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)

    objects = CartManager()

class EventInCart(models.Model):
    class Meta:
        unique_together = (('cart', 'event'),)
    event_in_cart_id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE)
    event = models.ForeignKey(Event, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField()




'''

class OtpModel(models.Model):
    otp_regex = RegexValidator( regex = r'^\d{6}$',message = "otp should be in six digits")
    otp = models.CharField(max_length=6, validators=[otp_regex])
    phone_regex = RegexValidator( regex = r'^\d{10}$',message = "phone number should exactly be in 10 digits")
    phone = models.CharField(max_length=255, validators=[phone_regex])
    expiry = models.DateTimeField(default = (timezone.now() + timedelta(minutes = 5)))
    is_verified = models.BooleanField(default=False)
    
'''    