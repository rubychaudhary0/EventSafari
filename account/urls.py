from django.urls import path
from . import views
from .views import RegistrationView

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('organizer_signup', RegistrationView.as_view(), name='organizer_signup'),
    
]