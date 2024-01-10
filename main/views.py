from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.generic import TemplateView, FormView, CreateView, ListView, UpdateView, DeleteView, DetailView, View
from django.core.exceptions import ValidationError
from .forms import  RegistrationForm, CartForm, CustomUserChangeForm, AudienceProfileForm
from django.urls import reverse_lazy, reverse
from .models import CustomUser, Event, Cart, EventInCart, Category
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.paginator import Paginator

from EventSafari import settings
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from django.contrib.postgres.search import SearchVector,  SearchQuery, SearchRank

from nbconvert import HTMLExporter
from nbformat import read
import os



import pickle 
import pandas as pd
# Create your views here.
  
def Index(request):
    event_data = Event.objects.all()
    context = {
        'event_data':event_data
    }
    return render(request, 'main/index.html', context)



#Search
def search(request): 
     return render(request, 'main/search.html')  


class SearchResultsList(ListView):
    model = Event
    context_object_name = "events"
    template_name = "main/search.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        search_vector = SearchVector("title", "event_description", "category", "venue")
        search_query = SearchQuery(query)
        return (
            Event.objects.annotate(
                search=search_vector, rank=SearchRank(search_vector, search_query)
            )
            .filter(search=search_query)
            .order_by("-rank")
        )

def testsessions(request):
    if request.session.get('test', False):
        print(request.session["test"])
    request.session['test'] = "testing"
    request.session['test2'] = "testing2"
    return render(request, "main/sessiontesting.html")


class RegisterView(CreateView):
    template_name = 'main/registerbasicuser.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('signup')

    def post(self, request, *args, **kwargs):
        user_email = request.POST.get('email')
        try:
            existing_user = CustomUser.objects.get(email = user_email)
            if(existing_user.is_active == False):
                existing_user.delete()
        except:
            pass
        response = super().post(request, *args, **kwargs)
        if response.status_code == 302:
            user = CustomUser.objects.get(email = user_email)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)     
            mail_subject = 'Activate your account.'
            message = render_to_string('main/authentication/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            
            to_email = user_email 
            form = self.get_form()
            try:
                send_mail(
                    subject=mail_subject,
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list= [to_email],
                    fail_silently=False,    
                )
                messages.success(request, "Link has been sent to your email id. please check your inbox and if its not there check your spam as well.")
                return self.render_to_response({'form':form})
            except:
                form.add_error('', 'Error Occured In Sending Mail, Try Again')
                messages.error(request, "Error Occured In Sending Mail, Try Again")
                return self.render_to_response({'form':form})
        else:
            return response
        

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist) as e:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, "Successfully Logged In")
        return redirect(reverse_lazy('index'))
    else:
        return HttpResponse('Activation link is invalid or your account is already Verified! Try To Login')

class LoginViewUser(LoginView):
    template_name = "main/login.html"

class LogoutViewUser(LogoutView):
    success_url = reverse_lazy('login')

@login_required
def profile(request):
    if request.method == 'POST':
        #u_form = CustomUserChangeForm(request.POST, instance=request.user)
        p_form = AudienceProfileForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if p_form.is_valid():
            #u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile') # Redirect back to profile page

    else:
        #u_form = CustomUserChangeForm(instance=request.user)
        p_form = AudienceProfileForm(instance=request.user.profile)

    context = {
        #'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'main/profile.html', context)

def event_list(request):
    events = Event.objects.all()
    paginator = Paginator(events, 4)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}

    if request.htmx:
        return render(request, 'main/partials/list.html', context)
    return render(request, 'main/listevents.html', context)



#recommended=pickle.load(open(".pkl",'rb'))
similarity=pickle.load(open("similarity.pkl",'rb'))
event_lists=pickle.load(open("event_list.pkl",'rb'))
df = pd.DataFrame(event_lists)

#print(event_lists)
    
def event_detail(request, event_id):
    # Get the event details based on the event ID
    event = get_object_or_404(Event, pk=event_id)
    

    filtered_df = df[df['title'] == event]
    
    if not filtered_df.empty:
        index = filtered_df.index[0]
        event_list = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])[1:6]
        
        recommended_events = [df.iloc[i[0]].title for i in event_lists]
    else:
        # Handle the case where the event is not found in the DataFrame
        index = None
        recommended_events = []
    
    return render(request, 'main/event_detail.html',  {'event': event, 'recommended_events': recommended_events})




def eventcategory(request):
    cat = Category.objects.all()
    context = {'cat': cat}
    return render(request, 'main/eventcategory.html', context)

def ReadCat(request, id):
    cats = Category.objects.get(cat_id = id)
    events = Event.objects.filter(category = cats)
    context = {'cat': cats, 'events': events}
    return render(request, 'main/read_cat.html', context)


@login_required
def addToCart(request, id):
    try:
        cart = Cart.objects.get(user = request.user)
        try:
            event = Event.objects.get(event_id = id)
            try:
                eventincart = EventInCart.objects.get(cart = cart, event = event)
                eventincart.quantity = eventincart.quantity + 1
                eventincart.save()
                messages.success(request, "Successfully added to cart")
                return redirect(reverse_lazy("displaycart"))
            except:
                eventincart = EventInCart.objects.create(cart = cart, event = event, quantity=1)
                messages.success(request, "Successfully added to cart")
                return redirect(reverse_lazy("displaycart"))
        except:
            messages.error(request, "Event can not be found")
            return redirect(reverse_lazy('listevents'))
    except:
        cart = Cart.objects.create(user = request.user)
        try:
            event = Event.objects.get(event_id = id)
            eventincart = EventInCart.objects.create(cart = cart, event = event, quantity = 1)
            messages.success(request, "Successfully added to cart")
            return redirect(reverse_lazy("displaycart"))
        except:
            messages.error(request, "Error in adding to cart. Please try again")
            return redirect(reverse_lazy('listevents'))

class DisplayCart(LoginRequiredMixin, ListView):
    model = EventInCart
    template_name = "main/displaycart.html"
    context_object_name = "cart"

    def get_queryset(self):
        queryset = EventInCart.objects.filter(cart = self.request.user.cart)
        return queryset


class UpdateCart(LoginRequiredMixin, UpdateView):
    model = EventInCart
    form_class = CartForm
    success_url = reverse_lazy("displaycart")

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 302:
            if int(request.POST.get("quantity")) == 0:
                eventincart = self.get_object()
                eventincart.delete()
            return response
        else:
            messages.error(request, "error in quantity")
            return redirect(reverse_lazy("displaycart"))

class DeleteFromCart(LoginRequiredMixin, DeleteView):
    model = EventInCart
    success_url = reverse_lazy("displaycart")  

