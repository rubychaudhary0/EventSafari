from django.urls import path
from . import views
from .views import EventCreationView, update_view, delete_view

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name="index"),
    path('signup/', views.RegisterView.as_view(), name="signup"),
    path('signuporganizer/', views.RegisterViewSeller.as_view(), name="signuporganizer"),
    path('login/', views.LoginViewUser.as_view(), name="login"),
    path('logout/', views.LogoutViewUser.as_view(), name="logout"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('home/', views.home, name="home"),
    path('events/', views.events, name="events"),
    path('create/', EventCreationView.as_view(),name='event-create'),
    path('<event_id>/edit/', update_view, name='edit_event'),
    path('<event_id>/delete/', delete_view, name='delete_event'),
    
]

urlpatterns += static(settings.MEDIA_URL ,document_root = settings.MEDIA_ROOT)