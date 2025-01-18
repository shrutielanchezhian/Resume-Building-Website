from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class CustomUserAdmin(UserAdmin):
    # Inherit the default fieldsets and add 'last_login' only once, if not already included.
    fieldsets = UserAdmin.fieldsets  # Use the original fieldsets from UserAdmin
    
    # Customize the add_fieldsets to include 'last_login' if it's not already included
    add_fieldsets = UserAdmin.add_fieldsets

# Unregister the default User model first
admin.site.unregister(User)

# Register the User model with your custom UserAdmin
admin.site.register(User, CustomUserAdmin)
