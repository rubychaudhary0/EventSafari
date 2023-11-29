from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, UserAdmin as BaseUserAdmin
from .forms import CustomUserAddForm, CustomUserChangeForm
from .models import CustomUser



@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserAddForm
    form = CustomUserChangeForm
    list_display = ('id', 'username', 'email')
    list_filter = ('is_admin', 'is_active', 'is_superuser', 'is_staff')
    readonly_fields = ['created_at', 'updated_at', 'last_login', 'created_by', 'uuid']
    search_fields = ('id', 'uuid', 'username', 'email')
    ordering = ('id', )
    fieldsets = (
        ('User', {'fields': ('uuid', 'username', 'email', 'password', 'created_by')}),
        ('Permissions', {'fields': ('is_active', 'is_superuser', 'is_admin', 'is_staff')}),
        ('Dates', {'fields': ('created_at', 'updated_at', 'last_login',)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "password", "confirm_password"),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)