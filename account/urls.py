from django.urls import path
from . import views
from .views import RegistrationView

urlpatterns = [
    path('', views.home, name='home'),
    path('audience/signup', views.signup, name='audience_signup'),
    path("audience/login", views.audience_login, name="audience_login"),
    path('logout', views.logout, name='logout'),
    path('organizer/signup', RegistrationView.as_view(), name='organizer_signup'),
    path("organizer/login", views.organizer_login, name="organizer_login"),
    
]