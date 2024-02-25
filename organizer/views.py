from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.views.generic import TemplateView, FormView, CreateView
from django.core.exceptions import ValidationError
from main.forms import RegistrationForm, RegistrationFormSeller2, EventCreation
from django.urls import reverse_lazy, reverse
from main.models import OrganizerAdditional, CustomUser, Event
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from bootstrap_datepicker_plus.widgets import DateTimePickerInput
# Create your views here.

def index(request):
    return render(request, 'organizer/index.html')

class LoginViewUser(LoginView):
    template_name = "organizer/login.html"
    success_url = reverse_lazy('dashboard')

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
    success_url = reverse_lazy('login')

class RegisterView(CreateView):
    template_name = 'organizer/registerbaseuser.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('dashboard')


@login_required
def dashboard(request):
    user_data = CustomUser.objects.all()
    context = {
        'user_data':user_data
    }
    return render(request, 'organizer/dashboard/dashboard.html', context)

def home(request):
    return render(request, 'organizer/dashboard/home.html')

def events(request):
    event = Event.objects.filter(organizer=request.user)
    return render(request, 'organizer/dashboard/events.html', {'event': event})


class OrganizerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.type and CustomUser.Types.ORGANIZER in self.request.user.type

    def handle_no_permission(self):
        return redirect('signuporganizer')

class EventCreationView(OrganizerRequiredMixin, CreateView):
    model = Event  
    form_class = EventCreation  
    template_name = 'organizer/create_event.html'
    success_url = reverse_lazy('dashboard')  

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        form.fields["pub_date"].widget = DateTimePickerInput()
        messages.success(self.request, "The event was created successfully.")
        return super().form_valid(form)


def update_view(request, event_id): 
    
    context ={}
 
    obj = get_object_or_404(Event, event_id = event_id)

    form = EventCreation(request.POST or None, instance = obj)
 
    if form.is_valid():
        form.save()
        return redirect(reverse_lazy('dashboard'))
 
    context["form"] = form
 
    return render(request, "organizer/update_view.html", context)


def delete_view(request, event_id):
    
    context ={}
 
    obj = get_object_or_404(Event, event_id = event_id)
 
 
    if request.method =="POST":
       
        obj.delete()
        
        return redirect(reverse_lazy('dashboard'))
 
    return render(request, "organizer/delete_view.html", context)