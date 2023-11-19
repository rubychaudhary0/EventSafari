from django.contrib.auth.backends import ModelBackend
from account.models import Audience, Organizer

class UserTypeBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            if kwargs['user_type'] == 'audience':
                user = Audience.objects.get(email=email)
            elif kwargs['user_type'] == 'organizer':
                user = Organizer.objects.get(email=email)
        except Audience.DoesNotExist, Organizer.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

    def get_user(self, user_id):
        try:
            return Audience.objects.get(pk=user_id)
        except Audience.DoesNotExist:
            try:
                return Organizer.objects.get(pk=user_id)
            except Organizer.DoesNotExist:
                return None
