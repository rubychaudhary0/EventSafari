import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .manager import AudienceManager


# Create your models here.
class Audience(AbstractUser):
    username = None 
    audience_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    email = models.EmailField(_('email address'), unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects = AudienceManager()
    
    def __str__(self):
        return self.email 
    


class Organizer(models.Model):
    organizer_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    org_name = models.CharField(max_length=50)
    org_description = models.TextField(max_length=500, blank=True)
    website_url = models.URLField(max_length=200, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    address = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    facebook = models.URLField(max_length=100, blank=True)
    instagram = models.URLField(max_length=100, blank=True)

    def __str__(self):
      return self.user.email
  

class Event(models.Model):
    event_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_name = models.CharField(max_length=150)
    event_description = models.TextField(max_length=500, blank=True)  
    event_date = models.DateTimeField(default=timezone.now)
    event_location = models.CharField(max_length=255, default='Default Location')
    event_capacity = models.IntegerField()
    event_price = models.FloatField()
    event_image = models.ImageField()
    organizer_id = models.ForeignKey(Organizer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    


class EventReview(models.Model):
    review_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    audience_id = models.ForeignKey(Audience, on_delete=models.CASCADE)
    review_text = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)


class Booking(models.Model):
    BOOKING_TYPE = (
        ("Reserve Event", "Reserve Event"),
        ("Buy Tickets", "Buy Tickets")
    )
    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    audience_id = models.ForeignKey(Audience, on_delete=models.CASCADE)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(default=timezone.now)
    booking_type = models.CharField(max_length=40, choices=BOOKING_TYPE, unique=True)
    ticket_quantity = models.IntegerField(default=1)
    total_price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)