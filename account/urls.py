from django.urls import path
from . import views
from .views import RegistrationView

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('audience/logout', views.audience_logout, name='audience_logout'),
    path('organizer_signup', RegistrationView.as_view(), name='organizer_signup'),
    
]