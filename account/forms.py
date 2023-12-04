from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from .models import CustomUser
from django.core.exceptions import ValidationError  
from django.contrib.auth.models import User


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