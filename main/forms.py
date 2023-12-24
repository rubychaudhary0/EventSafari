from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from .models import CustomUser, Organizer, OrganizerAdditional, Event, EventInCart
from django.core.exceptions import ValidationError 
from django.core.validators import RegexValidator
import zoneinfo

from timezone_field import TimeZoneFormField


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)



        
class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'email',
            'name',
            'password1',
            'password2',
        ]


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

class RegistrationFormSeller2(forms.ModelForm):
    class Meta:
        model = OrganizerAdditional
        fields = [
            'phone',
            'timezone'
        ]

class EventCreation(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title',
            'event_description',
            'start_date',
            'location',
            'capacity',
            'category',
            'image'
        ]


class CartForm(forms.ModelForm):
    class Meta:
        model = EventInCart
        fields = [
            'quantity'
        ]


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
