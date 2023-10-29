import uuid

from django.db import models
from django.utils import timezone
from account.models import Organizer, Audience

# Create your models here.
class Event(models.Model):
    EVENT_CATEGORY = (
        ("Music and Dance","Music and Dance"),
        ("Sports","Sports"),
        ("Religious","Religious"),
        ("Yoga and Meditation","Yoga and Meditation"),
        ("Other","Other")
    )
    event_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_name = models.CharField(max_length=150)
    event_description = models.TextField(max_length=500, blank=True)  
    event_date = models.DateTimeField(default=timezone.now)
    event_location = models.CharField(max_length=255, default='Default Location')
    event_capacity = models.IntegerField()
    event_category = models.CharField(max_length=100, choices=EVENT_CATEGORY, unique=True)
    event_price = models.DecimalField(max_digits=10, decimal_places=2)
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