from django.contrib import admin
<<<<<<< HEAD
from django.contrib.auth.admin import UserAdmin
from .models import User
=======
from User.models import User, Doctor, Patient
>>>>>>> aa1979b0426c63620f331414a9dd63dd206c0d3a
# Register your models here.


class CustomUserAdmin(UserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'id', 'first_name',
                    'last_name', 'date_of_birth', 'gender', 'phone', 'is_staff', 'is_active', 'is_superuser')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name',
         'date_of_birth', 'gender', 'phone', 'national_id', 'profileImgUrl')}),
        ('Permissions', {'fields': ('is_staff', 'is_active',
         'is_superuser')}),

    )
    # add_fieldsets is not a standard UserAdmin attribute. CustomUserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'gender', 'date_of_birth', 'phone', 'national_id', 'profileImgUrl', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser'),
        }),
    )
    search_fields = ('email', 'first_name',
                     'last_name', 'phone', 'national_id')
    ordering = ('email', 'id')
    filter_horizontal = ()


admin.site.register(User, CustomUserAdmin)
