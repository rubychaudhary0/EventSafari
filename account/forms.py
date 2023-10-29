from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from .models import Audience, Organizer
from django.core.exceptions import ValidationError  



# Registration form for Audience
class AudienceSignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200)

    class Meta:
        model = Audience
        fields = ('email', 'password1', 'password2')

class AudienceChangeForm(UserChangeForm):

    class Meta:
        model = Audience
        fields = ('email',) 



class OrganizerSignupForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    class Meta:
        model = Organizer
        fields = ('email', 'name', 'phone', 'date_of_birth', 'picture', 'password')

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Organizer
        fields = ('email', 'name', 'phone', 'location', 'is_staff', 'is_superuser')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user   

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Organizer
        fields = ('email', 'name', 'phone', 'date_of_birth', 'picture', 'password', 'is_active', 'is_superuser')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]     
      
""" 
# Registration form for Organizer
class OrganizerSignupForm(UserCreationForm):  
    accountname = forms.CharField(label=' Account Name', min_length=5, max_length=150)  
    email = forms.EmailField(label='Email')  
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)  
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)  
  
    def accountname_clean(self):  
        accountname = self.cleaned_data['accountname'].lower()  
        new = Organizer.objects.filter(accountname = accountname)  
        if new.count():  
            raise ValidationError("User Already Exists")  
        return accountname  
  
    def email_clean(self):  
        email = self.cleaned_data['email'].lower()  
        new = Organizer.objects.filter(email=email)  
        if new.count():  
            raise ValidationError(" Email Already Exists")  
        return email  
  
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("Password doesn't match")  
        return password2  
  
    def save(self, commit = True):  
        user = Organizer.objects.create_user(  
            self.cleaned_data['accountname'],  
            self.cleaned_data['email'],  
            self.cleaned_data['password1']  
        )  
        return user  
    

class OrganizerSignupForm(UserCreationForm):
    email = forms.EmailField(max_length=255)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    account_name = forms.CharField(max_length=50)
    phone_number = forms.CharField(max_length=20, required=False)
    city = forms.CharField(max_length=100, required=False)
    

    class Meta:
        model = Organizer
        fields = ('email', 'password1', 'password2', 'account_name', 'phone_number', 'city')

""" 
class EventFilterForm(forms.Form):
    location = forms.CharField(required=False)
    price = forms.DecimalField(required=False)
    date = forms.DateField(required=False)
    category = forms.CharField(required=False)