from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.views.generic import CreateView
from django.views.decorators.http import require_http_methods

from paypal.standard.forms import PayPalPaymentsForm

from .forms import CustomUserCreationForm
from .models import CustomUser, UserAppointment
from .tokens import account_activation_token


CITIES = ('City1', 'City2')
CENTERS = ('Center1', 'Center2', 'Center3', 'Center4')
MED_TYPE = ('Cardiology', 'Eye care', 'Psycology', 'Primary care')
DOCTORS = (
    {'Cardiolog1': ['Super cool', 15] , 'Cardiolog2': ['Amaizing', 12]},
    {'Eye Doc1': ['Nice', 11], 'Eye Doc2': ['Good one', 13]},
    {'Psycologist1': ['Trustfull', 13], 'Psycologist2': ['Gorgeous', 12]},
    {'Terapist1': ['Fabilous', 12], 'Terapist2': ['Spectacular', 14]}
)


def home(request):
    return render(request, "home.html", {"cities": CITIES})


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Thank you for your confirmation, you are now able to login')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid. Try again')
    return redirect('home')


def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account"
    message = render_to_string('registration/template_activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': "https" if request.is_secure() else "http" 
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'User {user} go to {to_email} and activate your email.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly')


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        activateEmail(self.request, user, form.cleaned_data.get('email'))
        return super().form_valid(form)


class Login(LoginView):
    template_name = 'registration/login.html'


@login_required
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
            description_list = dictionary.get(req)
            if description_list:
                description = description_list[0]
                price = description_list[1]
                str_descriprion = f'This doctor is {description}, Price: {price}'
                return HttpResponse(str_descriprion)


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
def create_appointment(request):
    if 'Open this menu' in [request.POST[i] for i in request.POST]:
        messages.error(request, 'Declined: Pick all fields.')
        return render(request, "home.html", {
            'cities': CITIES,
        })
    user_info, current_user = request.POST, request.user
    for item in DOCTORS:
        price = item.get(user_info.get('doctor-name'))
        if price:
            break
    user_object = CustomUser.objects.get(UserID=current_user.UserID)
    UserAppointment.objects.create(
        userid=user_object,
        AppCity=user_info.get('city'),
        AppClinicName=user_info.get('med-center'),
        AppMedCategory=user_info.get('med-type'),
        AppDoctor_Full_Name=user_info.get('doctor-name'),
        Price=int(price[1])
        )
    messages.success(request, 'your appointment was succesfully created')
    return render(request, "home.html", {"cities": CITIES})


@login_required
def user_appointments(request):
    current_user = request.user
    user_appointments = UserAppointment.objects.filter(userid=current_user)
    return render(request, 'user-appointments.html', {'appointments': user_appointments})


@require_http_methods(['DELETE'])
def delete_appointment(request, pk):
    current_user = request.user
    app = get_object_or_404(UserAppointment, userid_id=current_user, AppID=pk)
    app.delete()
    return redirect('user-appointments')


@login_required
def search(request):
    current_user = request.user
    user_appointments = UserAppointment.objects.filter(userid=current_user)
    if not request.GET.get('search'):
        return render(request, 'appointment-list.html', {'appointments': user_appointments})
    filtered = user_appointments.filter(AppID=int(request.GET.get('search')))
    return render(request, 'appointment-list.html', {'appointments': filtered})


@require_http_methods(['DELETE'])
def delete_user(request, pk):
    current_auth_user = vars(request.session).get('_session_cache').get('_auth_user_id')
    current_user = get_user_model().objects.get(UserID=pk)
    if int(current_auth_user) == current_user.UserID:
        current_user.is_active = False
        current_user.save()
        messages.success(request, 'Your account has been deleted')
        return redirect('home')
    else:
        messages.error(request, 'Forbidden, I"m CaLlInG tHe PoLiCe')
        return redirect('home')


def clear(request):
    return HttpResponse('')


@login_required
def order(request, app_id):
    order_obj = get_object_or_404(UserAppointment, AppID=app_id, userid_id=request.user)
    if order_obj.paid: 
        return redirect('home')
    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': str(order_obj.Price),
        'item_name': f'Appointment N#{order_obj.AppID}',
        'invoice': str(order_obj.AppID),
        'currency_code': 'USD',
        'notify_url': f'http://{host}{reverse("paypal-ipn")}',
        'return_url': f'http://{host}{reverse("paypal-return")}',
        'cancel_return': f'http://{host}{reverse("paypal-cancel")}',
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'process_payment.html', {'form': form, 'order_details': order_obj})


def paypal_return(request):
    messages.success(request, 'You\'ve successfully payed for an appointment!')
    return redirect('home')


def paypal_cancel(request):
    messages.error(request, 'Order has been cancelled')
    return redirect('home')
