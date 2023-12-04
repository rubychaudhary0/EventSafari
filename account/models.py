import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from PIL import Image
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField
from django.core.validators import RegexValidator

from django.db.models import Q
from datetime import timedelta

from .manager import CustomUserManager




class CustomUser(AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False
    )
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=50,
                                unique=True)
    name = models.CharField(null=True, blank=True, max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    phone_regex = RegexValidator( regex = r'^\d{10}$',message = "phone number should exactly be in 10 digits")
    phone = models.CharField(max_length=255, validators=[phone_regex], blank = True, null=True) 

    class Types(models.TextChoices):
        ORGANIZER = "Organizer", "ORGANIZER"
        AUDIENCE = "Audience", "AUDIENCE"
        

    default_type = Types.AUDIENCE

    type = MultiSelectField(choices=Types.choices, default=[], null=True, blank=True, max_length=9)
    

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.id}: {self.email}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.type.append(self.default_type)
        return super().save(*args, **kwargs)


class AudienceAdditional(models.Model):
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    profile_picture = models.ImageField(default='default.jpg', upload_to='profile_pics')


class OrganizerAdditional(models.Model):
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    profile_picture = models.ImageField(default='default.jpg', upload_to='profile_pics')
    website_url = models.URLField(max_length=200, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=200, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    
# Model Managers for proxy models
class OrganizerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        #return super().get_queryset(*args, **kwargs).filter(type = CustomUser.Types.SELLER)
        return super().get_queryset(*args, **kwargs).filter(Q(type__contains = CustomUser.Types.ORGANIZER))

class AudienceManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        #return super().get_queryset(*args, **kwargs).filter(type = CustomUser.Types.CUSTOMER)
        return super().get_queryset(*args, **kwargs).filter(Q(type__contains = CustomUser.Types.AUDIENCE))
       


# Proxy Models. They do not create a seperate table
class Organizer(CustomUser):
    default_type = CustomUser.Types.ORGANIZER
    objects = OrganizerManager()
    class Meta:
        proxy = True
    
    def sell(self):
        print("I can sell")

    @property
    def showAdditional(self):
        return self.selleradditional

class Audience(CustomUser):
    default_type = CustomUser.Types.AUDIENCE
    objects = AudienceManager()
    class Meta:
        proxy = True 

    def buy(self):
        print("I can buy")

    @property
    def showAdditional(self):
        return self.customeradditional

'''
class Audience(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(default='default.jpg', upload_to='profile_pics')


class Organizer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(default='default.jpg', upload_to='profile_pics')
    website_url = models.URLField(max_length=200, blank=True)
    phone = models.CharField(max_length=50)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=200, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
'''
        