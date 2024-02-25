from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from .models import CustomUser, Organizer, OrganizerAdditional, Event, EventInCart, AudienceAdditional
from django.core.exceptions import ValidationError 
from django.core.validators import RegexValidator
import zoneinfo

from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput

from timezone_field import TimeZoneFormField
from tinymce.widgets import TinyMCE

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)

class AudienceProfileForm(forms.ModelForm):
    class Meta:
        model = AudienceAdditional
        fields = ['profile_picture']

        
class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'email',
            'name',
            'password1',
            'password2',
        ]

'''
class RegistrationFormSeller(UserCreationForm):
    
    phone_regex = RegexValidator( regex = r'^\d{10}$',message = "phone number should exactly be in 10 digits")
    phone = forms.CharField(max_length=255, validators=[phone_regex])
    timezone = TimeZoneFormField(choices_display="WITH_GMT_OFFSET")
    class Meta:
        model = Organizer
        fields = [
            'email',
            'name',
            'password1',
            'password2',
            'phone',
            'timezone'
        ]        
'''

class RegistrationFormSeller2(forms.ModelForm):
    class Meta:
        model = OrganizerAdditional
        fields = [
            'phone',
            'address',
        ]

class EventCreation(forms.ModelForm):
    class Meta:
        model = Event
        widgets = {'content': TinyMCE(attrs={'cols': 40, 'rows': 20}),
                   "start_date": DatePickerInput(),
                   "end_date": DatePickerInput(range_from="start_date"),
                   "start_time": TimePickerInput(),
                   }
        fields = [
            'title',
            'event_description',
            'start_date',
            'end_date',
            'start_time',
            'category',
            'venue',
            'capacity',
            'image',
            'price'
        ]


class CartForm(forms.ModelForm):
    class Meta:
        model = EventInCart
        fields = [
            'quantity'
        ]

class PaymentForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
'''
class SendOtpBasicForm(forms.Form):
    phone_regex = RegexValidator( regex = r'^\d{10}$',message = "phone number should exactly be in 10 digits")
    phone = forms.CharField(max_length=255, validators=[phone_regex])

    class Meta:
        fields = [
            'phone',
        ]

class VerifyOtpBasicForm(forms.Form):
    otp_regex = RegexValidator( regex = r'^\d{4}$',message = "otp should be in six digits")
    otp = forms.CharField(max_length=6, validators=[otp_regex])

    # class Meta:
    #     field




'''
