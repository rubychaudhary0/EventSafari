from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, UserAdmin as BaseUserAdmin
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser, OrganizerAdditional,  Audience, Organizer, Event

class OrganizerAdditionalInline(admin.TabularInline):
    model = OrganizerAdditional

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'phone', 'name','type', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions',)}),   #'is_customer' , 'is_seller'
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'name', 'type', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


class OrganizerAdmin(admin.ModelAdmin):
    inlines = (
        OrganizerAdditionalInline,
    )

admin.site.register(CustomUser, CustomUserAdmin)    

'''
class ProductInCartInline(admin.TabularInline):
    model = ProductInCart

class CartInline(admin.TabularInline):
    model = Cart    #onetoonefield foreignkey

class DealInline(admin.TabularInline):
    model = Deal.user.through

@admin.register(Cart) # through register decorator
class CartAdmin(admin.ModelAdmin):
    model = Cart
    list_display = ('user','staff', 'created_on',)    # here user__is_staff will not work   
    list_filter = ('user', 'created_on',)
    #fields = ('staff',)           # either fields or fieldset
    fieldsets = (
        (None, {'fields': ('user', 'created_on',)}),   # only direct relationship no nested relationship('__') ex. user__is_staff
        #('User', {'fields': ('staff',)}),
    )
    inlines = (
        ProductInCartInline,
    )
    # To display only in list_display
    def staff(self,obj):
        return obj.user.is_staff
    # staff.empty_value_display = '???'
    staff.admin_order_field  = 'user__is_staff'  #Allows column order sorting
    staff.short_description = 'Staff User'  #Renames column head

    #Filtering on side - for some reason, this works
    list_filter = ['user__is_staff', 'created_on',]    # with direct foreign key(user) no error but not shown in filters, with function error
    # ordering = ['user',]
    search_fields = ['user__username']     # with direct foreign key no error but filtering not possible directly


class ProductInOrderInline(admin.TabularInline):
    model = ProductInOrder

@admin.register(Order) # through register decorator
class CartAdmin(admin.ModelAdmin):
    model = Cart
    inlines = (
        ProductInOrderInline,
    )
'''
#admin.site.register(Cart)
admin.site.register(Event)
#admin.site.register(ProductInCart)
#admin.site.register(Deal)#, DealAdmin)
#admin.site.register(UserType)
admin.site.register(Audience)
admin.site.register(Organizer, OrganizerAdmin)
admin.site.register(OrganizerAdditional)
