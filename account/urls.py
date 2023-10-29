from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('organizer_signup', views.organizer_signup, name='organizer_signup'),
    path('event', views.event, name='event'),
]