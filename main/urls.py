from django.contrib import admin
from django.views.generic import TemplateView, FormView, ListView, UpdateView, DeleteView, DetailView, CreateView
from django.urls import path, include
from . import views
from django.contrib import admin
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

from .views import SearchResultsList

urlpatterns = [
   
   
    
    path('', views.Index, name="index"),
    #path('search/', views.search, name="search"),
    
    path("search/", SearchResultsList.as_view(), name="search_results"),

    path('eventcategory/', views.eventcategory, name="eventcategory"),
    path('category/<int:id>', views.ReadCat, name="event-cat"),

    path('listevents/', views.ListEvents.as_view(), name="listevents"),
    path('eventdetail/<int:pk>/', views.EventDetail.as_view(), name="eventdetail"),
    path('addtocart/<int:id>/', views.addToCart, name="addtocart"),
    path('displaycart/', views.DisplayCart.as_view(), name="displaycart"),
    path('updatecart/<int:pk>/', views.UpdateCart.as_view(), name="updatecart"),
    path('deletefromcart/<int:pk>/', views.DeleteFromCart.as_view(), name="deletefromcart"),


    #path('api/listeventsapi/', views.listEventsApi, name="listeventsapi"),
   # path('api/suggestionapi/', views.suggestionApi, name="suggestionapi"),


    #authentication endpoints
    path('signup/', views.RegisterView.as_view(), name='signup'),
    path('login/', views.LoginViewUser.as_view(), name="login"),
    path('logout/', views.LogoutViewUser.as_view(), name="logout"),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),


    # change password
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='main/authentication/password_change_done.html'), 
        name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='main/authentication/password_change.html', success_url = reverse_lazy("password_change_done")), 
        name='password_change'),

    #Forgot password
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name = "main/authentication/password_reset_form.html", success_url = reverse_lazy("password_reset_complete")), 
    name="password_reset_confirm"),  # 3
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name = "main/authentication/password_reset.html", success_url = reverse_lazy("password_reset_done"), email_template_name = 'main/authentication/forgot_password_email.html'), 
    name="reset_password"),     # 1
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name = "main/authentication/password_reset_sent.html"), 
    name="password_reset_done"),    # 2
    
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name = "main/authentication/password_reset_done.html"), 
    name="password_reset_complete"),   # 4
    

    #recommendation
     path('notebook/', views.notebook_view, name='notebook'),


]

urlpatterns += static(settings.MEDIA_URL ,document_root = settings.MEDIA_ROOT)
