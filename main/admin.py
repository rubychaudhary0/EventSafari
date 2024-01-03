from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, UserAdmin as BaseUserAdmin
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser, OrganizerAdditional,  AudienceAdditional, Audience, Organizer, Event, Cart, EventInCart, Category

class OrganizerAdditionalInline(admin.TabularInline):
    model = OrganizerAdditional

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email',  'name','type', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions',)}),   #'is_customer' , 'is_seller'
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',  'name', 'type', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


class OrganizerAdmin(admin.ModelAdmin):
    inlines = (
        OrganizerAdditionalInline,
    )

admin.site.register(CustomUser, CustomUserAdmin)    



admin.site.register(Cart)
admin.site.register(Event)
admin.site.register(EventInCart)
admin.site.register(Category)
#admin.site.register(Deal)#, DealAdmin)
#admin.site.register(UserType)
admin.site.register(Audience)
admin.site.register(Organizer, OrganizerAdmin)
admin.site.register(OrganizerAdditional)
admin.site.register(AudienceAdditional)
