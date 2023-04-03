from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


#class CustomUserAdmin(UserAdmin):
#    add_form = CustomUserCreationForm
#    form = CustomUserChangeForm
#    model = CustomUser
#    list_display = ["username", "email"]

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('role',)}),
    )
    list_display = UserAdmin.list_display + ('role',)


admin.site.register(CustomUser, CustomUserAdmin)