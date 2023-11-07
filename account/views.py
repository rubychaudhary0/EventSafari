from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import AudienceSignupForm, OrganizerSignupForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse

from .models import Organizer

# Create your views here.

#the landing page
def home(request):
    return render(request, 'home.html')

#signup for audience
def signup(request):
    if request.method == 'POST':
        form = AudienceSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = AudienceSignupForm()
    return render(request, 'audience/signup.html', {'form': form})


def audience_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('home')



class RegistrationView(CreateView):
    template_name = 'organizer/organizer_signup.html'
    form_class = OrganizerSignupForm

    def get_context_data(self, *args, **kwargs):
        context = super(RegistrationView, self).get_context_data(*args, **kwargs)
        context['next'] = self.request.GET.get('next')
        return context

    def get_success_url(self):
        next_url = self.request.POST.get('next')
        success_url = reverse('login')
        if next_url:
            success_url += '?next={}'.format(next_url)

        return success_url
    
class ProfileView(UpdateView):
    model = Organizer
    fields = ['name', 'phone', 'description', 'picture']
    template_name = 'registration/profile.html'

    def get_success_url(self):
        return reverse('index')

    def get_object(self):
        return self.request.user    
