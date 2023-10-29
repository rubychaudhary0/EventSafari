from django.contrib.auth.base_user import BaseUserManager 
from django.utils.translation import gettext_lazy as _ 


class AudienceManager(BaseUserManager):
    """
   # Custom user model manager where email is the unique identifiers
    #for authentication instead of usernames.
    """
    
    def create_user(self, email, password, **extra_fields):
        """
      #  Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set !"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user 


    def create_superuser(self, email, password, **extra_fields):
            """
          #  Create and save a SuperUser with the given email and password.
            """
            extra_fields.setdefault("is_active", True)
            extra_fields.setdefault("is_staff", True)
            extra_fields.setdefault("is_superuser", True)
            
            if extra_fields.get("is_staff") is not True:
                raise ValueError(_("Superuser must have is_staff=True"))
            if extra_fields.get("is_superuser") is not True:
                raise ValueError(_("Superuser must have is_superuser=True"))
            return self.create_user(email, password, **extra_fields)
    

class OrganizerManager(BaseUserManager):
     use_in_migrations = True

     def _create_user(self, email, name, phone, password, **extra_fields):
        values = [email, name, phone]
        field_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))
        for field_name, value in field_value_map.items():
            if not value:
                raise ValueError('The {} value must be set'.format(field_name))

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            name=name,
            phone=phone,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

     def create_user(self, email, name, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, name, phone, password, **extra_fields)

     def create_superuser(self, email, name, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, name, phone, password, **extra_fields)
