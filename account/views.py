from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import RegistrationForm

# Create your views here.

#the landing page
def home(request):
    return render(request, 'home.html')


class RegisterView(CreateView):
    template_name = 'account/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('home')
