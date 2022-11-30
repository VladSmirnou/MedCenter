from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Employee, CustomUser, UserAccount, UserTransaction, UserAppointment


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "UserID",
        "username",
        "UserFirst_Name",
        "UserLast_Name",
        "UserMobile_Phone",
        "UserEmail",
        "is_staff",
    ]
    fieldsets = UserAdmin.fieldsets + (
        (
            None,
            {
                "fields": (
                    "UserFirst_Name",
                    "UserLast_Name",
                    "UserMobile_Phone",
                    "UserEmail",
                )
            },
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            None,
            {
                "fields": (
                    "UserFirst_Name",
                    "UserLast_Name",
                    "UserMobile_Phone",
                    "UserEmail",
                )
            },
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Employee, UserAccount, UserTransaction, UserAppointment)
class RegAdmin(admin.ModelAdmin):
    pass
