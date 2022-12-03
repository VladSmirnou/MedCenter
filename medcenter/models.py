from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from .validators import validate_email, validate_phone, validate_users
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    UserID = models.BigAutoField(primary_key=True)
    first_name = models.CharField(
        max_length=32,
        validators=[validate_users],
        db_column="UserFirst_Name",
        verbose_name="First name",
        help_text=_(
        "This fields is required. Should be more than or equal to 5 \
        and less than or equal to 25 characters. Accepts only lower and upper letters and digits."
        ),
    )
    last_name = models.CharField(
        max_length=32,
        validators=[validate_users],
        db_column="UserLast_Name",
        verbose_name="Last name",
        help_text=_(
        "This fields is required. Should be more than or equal to 5 \
        and less than or equal to 25 characters. Accepts only lower and upper letters and digits."
        ),
    )
    UserMobile_Phone = models.CharField(
        max_length=32,
        validators=[validate_phone],
        blank=True,
        verbose_name="Mobile phone",
        help_text=_(
            "Not required. Standart format is -> +XXX (XX) XXX-XXX-XXXX"
        ),
    )
    email = models.EmailField(
        max_length=128,
        validators=[validate_email],
        blank=True,
        db_column='UserEmail',
    )

    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return f"User ID: {self.UserID}"


class Employee(models.Model):
    EmpID = models.BigAutoField(primary_key=True)
    EmpFirst_Name = models.CharField(max_length=30)
    EmpLast_Name = models.CharField(max_length=30)
    EmpMobile_Phone = models.CharField(max_length=30)
    EmpEmail = models.CharField(max_length=100)
    EmpPicture = models.ImageField(default="default.jpg", upload_to="emp_photos")
    Salary = models.FloatField()
    ManagerID = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"Employee ID: {self.EmpID}; Full name: {self.EmpFirst_Name} {self.EmpLast_Name}"


class UserAccount(models.Model):
    Account_ID = models.BigAutoField(primary_key=True)
    userid = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    Account_Type = models.CharField(max_length=6)
    Balance = models.FloatField(default=0)

    def __str__(self):
        return f"Account ID: {self.Account_ID}, {self.userid}"


class UserTransaction(models.Model):
    TransactionID = models.BigAutoField(primary_key=True)
    account_id = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    empid = models.ForeignKey(
        Employee, null=True, blank=True, on_delete=models.SET_NULL
    )
    Transaction_time = models.DateTimeField(default=timezone.now)
    Transaction_amount = models.FloatField()

    def __str__(self):
        return f"Transaction ID: {self.TransactionID}, {self.account_id}"


class UserAppointment(models.Model):
    AppID = models.BigAutoField(primary_key=True)
    empid = models.ForeignKey(
        Employee, null=True, blank=True, on_delete=models.SET_NULL
    )
    userid = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    AppCity = models.CharField(max_length=20)
    AppClinicName = models.CharField(max_length=20)
    AppMedCategory = models.CharField(max_length=40)
    AppDoctor_Full_Name = models.CharField(max_length=30)
    