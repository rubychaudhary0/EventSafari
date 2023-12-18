from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import TemplateView, FormView, CreateView
from django.core.exceptions import ValidationError
from main.forms import RegistrationForm, RegistrationFormSeller2
from django.urls import reverse_lazy, reverse
from main.models import OrganizerAdditional, CustomUser
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

def index(request):
    return render(request, 'organizer/index.html')

class LoginViewUser(LoginView):
    template_name = "organizer/login.html"
    #success_url = reverse_lazy('index')

class RegisterViewSeller(LoginRequiredMixin, CreateView):
    template_name = 'organizer/register.html'
    form_class = RegistrationFormSeller2
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = self.request.user
        user.type.append(user.Types.ORGANIZER)
        user.save()
        form.instance.user = self.request.user
        return super().form_valid(form)
        

class LogoutViewUser(LogoutView):
    success_url = reverse_lazy('index')

class RegisterView(CreateView):
    template_name = 'organizer/registerbaseuser.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('index')