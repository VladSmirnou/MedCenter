from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class CustomUser(AbstractUser):
    UserID = models.BigAutoField(primary_key=True)
    UserFirst_Name = models.CharField(max_length=30)
    UserLast_Name = models.CharField(max_length=30)
    UserMobile_Phone = models.CharField(max_length=30)
    UserEmail = models.CharField(max_length=100)
    REQUIRED_FIELDS = ["UserFirst_Name", "UserLast_Name"]

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
