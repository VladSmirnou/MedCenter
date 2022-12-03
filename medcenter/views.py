from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import UserAccount, CustomUser, UserAppointment, UserTransaction
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LoginView


CITIES = ('City1', 'City2')
CENTERS = ('Center1', 'Center2', 'Center3', 'Center4')
MED_TYPE = ('Cardiology', 'Eye care', 'Psycology', 'Primary care')
DOCTORS = (
    {'Cardiolog1': 'Super cool' , 'Cardiolog2': 'Amaizing'},
    {'Eye Doc1': 'Nice', 'Eye Doc2': 'Good one'},
    {'Psycologist1': 'Trustfull', 'Psycologist2': 'Gorgeous'},
    {'Terapist1': 'Fabilous', 'Terapist2': 'Spectacular'}
)


def home(request):
    return render(request, "home.html", {"cities": CITIES})


def chain_drop(request):
    
    '''
                ~~ configures chained drop-down ~~

        This function and the dummy db on top of this module
    were created just for presentation purposes. 
        In this particular case it allows to avoid using
    too many unnecessary urls, functions and models.
    '''
    # exception block
    if request.GET.get('city') == 'Open this menu':
        return render(request, "partials/med-center.html")
    elif request.GET.get('med-center') == 'Open this menu':
        return render(request, "partials/med-type.html")
    elif request.GET.get('med-type') == 'Open this menu':
        return render(request, "partials/doctor-name.html")
    elif request.GET.get('doctor-name') == 'Open this menu':
        return HttpResponse('')

    #city block
    match request.GET.get('city'):
        case 'City1':
            return render(request, 'partials/med-center.html', {'centers': CENTERS[:2]})
        case 'City2':
            return render(request, 'partials/med-center.html', {'centers': CENTERS[2:]})

    #med-center block
    if request.GET.get('med-center') in CENTERS[:2]:
        return render(request, 'partials/med-type.html', {'types': MED_TYPE[:2]})
    elif request.GET.get('med-center') in CENTERS[2:]:
        return render(request, 'partials/med-type.html', {'types': MED_TYPE[2:]})

    #med-type block
    if request.GET.get('med-type') in MED_TYPE[:2]:
        if request.GET.get('med-type') == 'Cardiology':
            return render(request, 'partials/doctor-name.html', {'doctors': DOCTORS[0]})
        elif request.GET.get('med-type') == 'Eye care':
            return render(request, 'partials/doctor-name.html', {'doctors': DOCTORS[1]})
    elif request.GET.get('med-type') in MED_TYPE[2:]:
        if request.GET.get('med-type') == 'Psycology':
            return render(request, 'partials/doctor-name.html', {'doctors': DOCTORS[2]})
        elif request.GET.get('med-type') == 'Primary care':
            return render(request, 'partials/doctor-name.html', {'doctors': DOCTORS[3]})
    
    #description block
    if (req:= request.GET.get('doctor-name')):
        for dictionary in DOCTORS:
            description = dictionary.get(req)
            if description:
                return HttpResponse(description)


@login_required
def user_details(request):
    current_user = request.user
    return render(request, 'user-details.html', {
    'fname': current_user.first_name,
    'lname': current_user.last_name,
    'email': current_user.email,
    'mobile': current_user.UserMobile_Phone
    })


@login_required
def user_accounts(request):
    current_user = request.user
    user_accounts = UserAccount.objects.filter(userid=current_user)
    return render(request, 'user-accounts.html', {'accounts': user_accounts})


@login_required
def create_account(request):
    current_user = request.user
    if request.method == 'GET':
        user_accounts = UserAccount.objects.filter(userid=current_user)
        return render(request, 'create-account.html', {'accounts': user_accounts})
    account_type = request.POST.get('account-type')
    UserAccount.objects.create(userid=current_user, Account_Type=account_type)
    messages.success(request, f'Your {account_type} account was successfully created')
    return redirect('user-details')


@login_required
def account_details(request, pk):
    user_account = UserAccount.objects.get(pk=pk)
    return render(request, 'account-details.html', {'account': user_account})


@login_required
def create_appointment(request):
    # add the success signal in html
    # maybe change POST method to PUT later
    if 'Open this menu' in [request.POST[i] for i in request.POST]:
        return render(request, "home.html", {
            'cities': CITIES,
            'declined': 'Declined: Pick all fields.'
        })
    user_info, current_user = request.POST, request.user
    user_object = CustomUser.objects.get(UserID=current_user.UserID)
    UserAppointment.objects.create(
        userid=user_object,
        AppCity=user_info.get('city'),
        AppClinicName=user_info.get('med-center'),
        AppMedCategory=user_info.get('med-type'),
        AppDoctor_Full_Name=user_info.get('doctor-name')
        )
    return render(request, "home.html", {"cities": CITIES})


@login_required
def user_appointments(request):
    current_user = request.user
    user_appointments = UserAppointment.objects.filter(userid=current_user)
    return render(request, 'user-appointments.html', {'appointments': user_appointments})


@login_required
@require_http_methods(['DELETE'])
def delete_appointment(request, pk):
    # EVEN THO A MAN THAT IS NOT LOGGED IN CAN'T
    # DELETE AN APPOINTMENT, LOGGED IN USER STILL
    # CAN DELETE ANOTHER USER APPOINTMENTS BY TYPING
    # PROPER URL. DONT FORGET TO FIX THAT HERE AND 
    # IN ANOTHER VIEWS AS WELL.
    UserAppointment.objects.get(AppID=pk).delete()
    return redirect('user-appointments')


def transactions(request, pk):
    # doesn't work properly
    # don't fix this, add fake 3rd party transactions
    if request.method == 'GET':
        user_account = UserAccount.objects.get(Account_ID=pk) 
        return render(request, 'transaction.html', {'account': user_account})
    user_account = UserAccount.objects.get(Account_ID=pk)
    UserTransaction.objects.create(
        account_id=user_account,
        Transaction_amount=(amount:= float(request.POST.get('amount'))))
    user_account.Balance += amount
    user_account.save()
    return render(request, 'account-details.html', {'account': user_account})


def account_transfer(request, pk):
    # doesn't work properly
    # don't fix this, add fake 3rd party transactions
    if request.method == 'GET':
        user_account = UserAccount.objects.get(Account_ID=pk) 
        return render(request, 'transfer.html', {'account': user_account})
    user_accounts = UserAccount.objects.filter(userid=request.user)
    for account in user_accounts:
        if account.Account_Type == 'Debit':
            account.Balance -= float(request.POST.get('amount'))
            if account.Balance < 0:
                user_account = UserAccount.objects.get(Account_ID=pk)
                return render(request, 'transfer.html', {'account': user_account, 'negative': True})
            account.save()
        else:
            account.Balance += float(request.POST.get('amount'))
            account.save()
    user_account = UserAccount.objects.get(Account_ID=pk)
    return render(request, 'account-details.html', {'account': user_account})


def search(request):
    current_user = request.user
    user_appointments = UserAppointment.objects.filter(userid=current_user)
    if not request.GET.get('search'):
        return render(request, 'appointment-list.html', {'appointments': user_appointments})
    filtered = user_appointments.filter(AppID=int(request.GET.get('search')))
    return render(request, 'appointment-list.html', {'appointments': filtered})


def delete_user(request, pk):
    # check if a user has money on balance, if does -> do not allow to delete
    CustomUser.objects.get(UserID=pk).delete()
    return redirect('home')


def clear(request):
    return HttpResponse('')


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class Login(LoginView):
    template_name = 'registration/login.html'