from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    

    #authentication endpoints
    path('signup', views.RegisterView.as_view(), name='signup'),
]