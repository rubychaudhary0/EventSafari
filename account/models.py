import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin, Group, Permission
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .manager import AudienceManager, OrganizerManager


# Create your models here.
class Audience(AbstractUser):
    username = None 
    audience_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    groups = models.ManyToManyField(Group, related_name='audience_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='audience_user_permissions')
    email = models.EmailField(_('email address'), unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects = AudienceManager()
    
    def __str__(self):
        return self.email 
    


class Organizer(AbstractBaseUser, PermissionsMixin):
    username = None
    organizer_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    groups = models.ManyToManyField(Group, related_name='organizer_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='organizer_user_permissions')
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=150)
    description = models.TextField(max_length=500, blank=True)
    website_url = models.URLField(max_length=200, blank=True)
    phone_number = models.CharField(max_length=50)
    address = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    picture = models.ImageField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True)

    objects = OrganizerManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name.split()[0]

  

