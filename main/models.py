import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from PIL import Image
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField
from django.core.validators import RegexValidator


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
    uuid = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False
    )
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


class Event(models.Model):
    EVENT_CATEGORY = (
        ("Music and Dance","Music and Dance"),
        ("Sports","Sports"),
        ("Religious","Religious"),
        ("Yoga and Meditation","Yoga and Meditation"),
        ("Other","Other")
    )
    event_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=150)
    event_description = models.TextField(max_length=500, blank=True)  
    event_date = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=255, default='Default Location')
    capacity = models.IntegerField()
    category = models.CharField(max_length=100, choices=EVENT_CATEGORY, unique=True)
    image = models.ImageField(default="default_banner.png", upload_to="event_images")
    creator = models.ForeignKey(Organizer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
	     return f'{self.event_name}'
    
'''
class Ticket(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    ticket_name = models.CharField(max_length=15)
    ticket_description = models.TextField(max_length=500, blank=True) 
    price = models.FloatField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date_added = models.DateTimeField(default=timezone.now)

    #class Meta:
        #ordering = ['-price']      # default ordering whenever you query to database    retrieval in order as stored in DB ---> ordering ---> returned as a queryset where called

    @classmethod
    def updateprice(cls,ticket_id, price):
        ticket = cls.objects.filter(ticket_id = ticket_id)
        ticket = ticket.first()
        ticket.price = price
        ticket.save()
        return ticket

    @classmethod
    def create(cls, ticket_name, price):
        ticket = Ticket(ticket_name = ticket_name, price = price)
        ticket.save()
        return ticket
    
    def __str__(self):
        return self.ticket_name



class CartManager(models.Manager):
    def create_cart(self, user):
        cart = self.create(user = user)
        return cart

class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)

    objects = CartManager()

class ProductInCart(models.Model):
    class Meta:
        unique_together = (('cart', 'product'),)
    product_in_cart_id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE)
    product = models.ForeignKey(Ticket, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField()


class Order(models.Model):
    status_choices = (
        (1, 'Not Packed'),
        (2, 'Ready For Shipment'),
        (3, 'Shipped'),
        (4, 'Delivered')
    )
    payment_status_choices = (
        (1, 'SUCCESS'),
        (2, 'FAILURE' ),
        (3, 'PENDING'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.IntegerField(choices = status_choices, default=1)

    total_amount = models.FloatField()
    payment_status = models.IntegerField(choices = payment_status_choices, default=3)
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True, default=None) 
    datetime_of_payment = models.DateTimeField(default=timezone.now)
    
    
    

    def save(self, *args, **kwargs):
        if self.order_id is None and self.datetime_of_payment and self.id:
            self.order_id = self.datetime_of_payment.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.user.email + " " + str(self.id)
    

class ProductInOrder(models.Model):
    class Meta:
        unique_together = (('order', 'product'),)
    order = models.ForeignKey(Order, on_delete = models.CASCADE)
    product = models.ForeignKey(Ticket, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField()




class Deal(models.Model):
    user = models.ManyToManyField(CustomUser)
    deal_name = models.CharField(max_length=255)



class OtpModel(models.Model):
    otp_regex = RegexValidator( regex = r'^\d{6}$',message = "otp should be in six digits")
    otp = models.CharField(max_length=6, validators=[otp_regex])
    phone_regex = RegexValidator( regex = r'^\d{10}$',message = "phone number should exactly be in 10 digits")
    phone = models.CharField(max_length=255, validators=[phone_regex])
    expiry = models.DateTimeField(default = (timezone.now() + timedelta(minutes = 5)))
    is_verified = models.BooleanField(default=False)
    
'''    