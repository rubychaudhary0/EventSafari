from django.contrib import admin
from .models import Event, EventReview, Booking

# Register your models here.
admin.site.register(Event)
admin.site.register(EventReview)
admin.site.register(Booking)


