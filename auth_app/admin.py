# Register your models here.

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from auth_app.models import User
from auth_app.forms import AuthUserCreationForm, AuthUserChangeForm

class UserAdmin ( BaseUserAdmin ):
    # The forms to add and change user instances
    form = AuthUserChangeForm
    add_form = AuthUserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ( 'email', 'date_of_birth', 'is_admin' )
    list_filter = ( 'is_admin', )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('date_of_birth',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'date_of_birth', 'password1', 'password2')}
        ),
    )
    
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register( User, UserAdmin )
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister( Group )