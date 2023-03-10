from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Employee, CustomUser, UserAppointment


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "username",
        "first_name",
        "last_name",
        "UserMobile_Phone",
        "email",
        "is_staff",
    ]
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("UserMobile_Phone",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ('first_name', 'last_name', 'UserMobile_Phone', 'email')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Employee, UserAppointment)
class RegAdmin(admin.ModelAdmin):
    pass
