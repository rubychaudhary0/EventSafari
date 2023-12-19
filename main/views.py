from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.views.generic import TemplateView, FormView, CreateView, ListView, UpdateView, DeleteView, DetailView, View
from django.core.exceptions import ValidationError
from .forms import RegistrationFormSeller, RegistrationForm, RegistrationFormSeller2
from django.urls import reverse_lazy, reverse
from .models import CustomUser, Event
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin


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

# Create your views here.
'''
#the landing page
def home(request):
    return render(request, 'home.html')

'''    
def Index(request):
    event_data = Event.objects.all()
    print(event_data)
    context = {
        'event_data':event_data
    }
    return render(request, 'main/index.html', context)

'''
class Index(TemplateView):
    template_name = 'main/index.html'

    def data(self, request, *args, **kwargs):
        event_data = Event.objects.all()
        print(event_data)
        context = {
           'event_data':event_data
        }
'''

class search(TemplateView):
    template_name = 'main/search.html'    


def testsessions(request):
    if request.session.get('test', False):
        print(request.session["test"])
    #request.session.set_expiry(1)
    # if request.session['test']:
    #     print(request.session['test'])
    request.session['test'] = "testing"
    request.session['test2'] = "testing2"
    return render(request, "main/sessiontesting.html")


class RegisterView(CreateView):
    template_name = 'main/registerbasicuser.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('signup')

    def post(self, request, *args, **kwargs):
        #form = RegistrationForm(request.POST)
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
            message = render_to_string('main/registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            #print(message)
            to_email = user_email   
            #form = RegistrationForm(request.POST)   # here we are again calling all its validations
            form = self.get_form()
            try:
                send_mail(
                    subject=mail_subject,
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list= [to_email],
                    fail_silently=False,    # if it fails due to some error or email id then it get silenced without affecting others
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
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid or your account is already Verified! Try To Login')

class LoginViewUser(LoginView):
    template_name = "main/login.html"

class LogoutViewUser(LogoutView):
    success_url = reverse_lazy('index')


class ListEvents(ListView):
    template_name = "main/listevents.html"
    model = Event
    context_object_name = "event"
    paginate_by = 2



from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
EVENTS_PER_PAGE = 2
def listEvents(request):
    
    location = request.GET.get('location', "")     # http://www.wondershop.in:8000/listproducts/?page=1&ordering=price
    search = request.GET.get('search', "")
    category = request.GET.get('category', "")

    if search:
        event = Event.objects.filter(Q(event_name__icontains=search) | Q(location__icontains=search)) # SQLite doesn’t support case-sensitive LIKE statements; contains acts like icontains for SQLite

    else:
        event = Event.objects.all()

    if location:
        event = event.filter(location__lt = location)

    if category:
        event = event.filter(category__lt = category)
    

    # Pagination
    page = request.GET.get('page',1)
    event_paginator = Paginator(event, EVENTS_PER_PAGE)
    try:
        event = event_paginator.page(page)
    except EmptyPage:
        event = event_paginator.page(event_paginator.num_pages)
    except:
        event = event_paginator.page(EVENTS_PER_PAGE)
    return render(request, "main/events.html", {"event":event, 'page_obj':event, 'is_paginated':True, 'paginator':event_paginator})


def suggestionApi(request):
    if 'term' in request.GET:
        search = request.GET.get('term')
        qs = Event.objects.filter(Q(event_name__icontains=search))[0:10]
        # print(list(qs.values()))
        # print(json.dumps(list(qs.values()), cls = DjangoJSONEncoder))
        titles = list()
        for event in qs:
            titles.append(event.event_name)
        #print(titles)
        if len(qs)<10:
            length = 10 - len(qs)
            qs2 = Event.objects.filter(Q(brand__icontains=search))[0:length]
            for event in qs2:
                titles.append(event.location)
        return JsonResponse(titles, safe=False)      # [1,2,3,4] ---> "[1,2,3,4]"   queryset ---> serialize into list or dict format ---> json format using json.dumps with a DjangoJSONEncoder(encoder to handle datetime like objects)




def listEventsApi(request):
    # print(Product.objects.all())
    # print(Product.objects.values())
    #result = json.dumps(list(Product.objects.values()), sort_keys=False, indent=0, cls=DjangoJSONEncoder)   # will return error if you have a datetime object as it is not jsonserializable  so thats why use DjangoJSONEncoder, indent to beautify and sort_keys to sort keys
    #print(type(result))    #str type  
    #print(result)
    result = list(Event.objects.values())          # will work like passing queryset as a context data if used by a template
    #print(result)
    #return render(request, "firstapp/listproducts.html", {"product":result})
    return JsonResponse(result, safe=False)




class EventDetail(DetailView):
    model = Event
    template_name = "main/event_detail.html"
    context_object_name = "event"

'''
@login_required
def addToCart(request, id):
    try:
        cart = Cart.objects.get(user = request.user)
        try:
            product = Product.objects.get(product_id = id)
            try:
                productincart = ProductInCart.objects.get(cart = cart, product = product)
                productincart.quantity = productincart.quantity + 1
                productincart.save()
                messages.success(request, "Successfully added to cart")
                return redirect(reverse_lazy("displaycart"))
            except:
                productincart = ProductInCart.objects.create(cart = cart, product = product, quantity=1)
                messages.success(request, "Successfully added to cart")
                return redirect(reverse_lazy("displaycart"))
        except:
            messages.error(request, "Product can not be found")
            return redirect(reverse_lazy('listproducts'))
    except:
        cart = Cart.objects.create(user = request.user)
        try:
            product = Product.objects.get(product_id = id)
            productincart = ProductInCart.objects.create(cart = cart, product = product, quantity = 1)
            messages.success(request, "Successfully added to cart")
            return redirect(reverse_lazy("displaycart"))
        except:
            messages.error(request, "Error in adding to cart. Please try again")
            return redirect(reverse_lazy('listproducts'))


class DisplayCart(LoginRequiredMixin, ListView):
    model = ProductInCart
    template_name = "account/displaycart.html"
    context_object_name = "cart"

    def get_queryset(self):
        queryset = ProductInCart.objects.filter(cart = self.request.user.cart)
        return queryset

class UpdateCart(LoginRequiredMixin, UpdateView):
    model = ProductInCart
    form_class = CartForm
    success_url = reverse_lazy("displaycart")

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 302:
            if int(request.POST.get("quantity")) == 0:
                productincart = self.get_object()
                productincart.delete()
            return response
        else:
            messages.error(request, "error in quantity")
            return redirect(reverse_lazy("displaycart"))

class DeleteFromCart(LoginRequiredMixin, DeleteView):
    model = ProductInCart
    success_url = reverse_lazy("displaycart")  
'''