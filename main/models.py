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
from tinymce import models as tinymce_models
from datetime import timedelta

import zoneinfo


from phonenumber_field.modelfields import PhoneNumberField

from .manager import CustomUserManager


class LowercaseEmailField(models.EmailField):
    def to_python(self, value):
        value = super(LowercaseEmailField, self).to_python(value)
        # Value can be None so check that it's a string before lowercasing.
        if isinstance(value, str):
            return value.lower()
        return value

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = LowercaseEmailField(_('email address'), unique=True)
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

    type = MultiSelectField(choices=Types.choices, default=[], null=True, blank=True, max_length=20)
    

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

    def __str__(self):
        return f'{self.user.name} Profile'

    # Override the save method of the model
    def save(self):
        super().save()

        img = Image.open(self.image.path) # Open image

        # resize image
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size) # Resize image
            img.save(self.image.path) # Save it again and override the larger image 

            
class OrganizerAdditional(models.Model):
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    address = models.CharField(max_length=255)
    website_url = models.URLField(max_length=200, blank=True)
    profile_picture = models.ImageField(default='default.jpg', upload_to='profile_pics')
    description = models.TextField(blank=True, null=True)
    social_media_link = models.URLField(blank=True, null=True)
    phone = PhoneNumberField()

    

    
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
    
    def create(self):
        print("I can create")

    @property
    def showAdditional(self):
        return self.organizeradditional

class Audience(CustomUser):
    default_type = CustomUser.Types.AUDIENCE
    objects = AudienceManager()
    class Meta:
        proxy = True 

    def book(self):
        print("I can book")

    @property
    def showAdditional(self):
        return self.audienceadditional

class Category(models.Model):
    cat_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150,db_index=True)
    
    def __str__(self):
        return self.name
    

class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150)
    event_description = tinymce_models.HTMLField() 
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    start_time = models.TimeField(default=timezone.now)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    venue = models.CharField(max_length=150)
    capacity = models.IntegerField()
    image = models.ImageField(default="default_banner.png", upload_to="event_images")
    price = models.FloatField(default=0)
    organizer = models.ForeignKey(Organizer, related_name='organizer', on_delete=models.CASCADE)
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

    def subtotal(self):
        events_in_cart = EventInCart.objects.filter(cart=self)
        total = 0
        for event_in_cart in events_in_cart:
            total += event_in_cart.event.price * event_in_cart.quantity
        return total

    def __str__(self):
	    return f"Cart for {self.user.name}"

class EventInCart(models.Model):
    class Meta:
        unique_together = (('cart', 'event'),)
    event_in_cart_id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE)
    event = models.ForeignKey(Event, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField()


    def __str__(self):
	     return f"Event: {self.event.title}"


class Payment(models.Model):
    pidx = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    mobile = models.CharField(max_length=20)
    purchase_order_id = models.CharField(max_length=100)
    purchase_order_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20)

'''

class OtpModel(models.Model):
    otp_regex = RegexValidator( regex = r'^\d{6}$',message = "otp should be in six digits")
    otp = models.CharField(max_length=6, validators=[otp_regex])
    phone_regex = RegexValidator( regex = r'^\d{10}$',message = "phone number should exactly be in 10 digits")
    phone = models.CharField(max_length=255, validators=[phone_regex])
    expiry = models.DateTimeField(default = (timezone.now() + timedelta(minutes = 5)))
    is_verified = models.BooleanField(default=False)
    
'''    