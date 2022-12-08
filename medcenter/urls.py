from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views 
from django.urls import path
from medcenter.utils import inactive_user_clean

from .views import (
    activate,
    chain_drop,
    create_appointment,
    clear,
    delete_appointment,
    delete_user,
    home,
    Login,
    order,
    paypal_return,
    paypal_cancel,
    search,
    SignUpView,
    user_details,
    user_appointments,
    )


urlpatterns = [
    path('', home, name='home'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-reset/',
    auth_views.PasswordResetView.as_view(
        template_name='password_reset_templates/password_reset.html'),
        name='password_reset'
    ),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_templates/password_reset_done.html'),
        name='password_reset_done'
    ),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_templates/password_reset_confirm.html'),
        name='password_reset_confirm'
    ),
    path('password-reset-complete/',
    auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_templates/password_reset_complete.html'),
        name='password_reset_complete'
    ),
    path('order/<int:app_id>/', order, name='order'),
    path('paypal-return/', paypal_return, name='paypal-return'),
    path('paypal-cancel/', paypal_cancel, name='paypal-cancel'),
]


htmx_patterns = [
    path('chain-drop/', chain_drop, name='chain-drop'),
    path('user-details/', user_details, name='user-details'),
    path('create-appointment/', create_appointment, name='create-appointment'),
    path('user-appointments/', user_appointments, name='user-appointments'),
    path('delete-appointment/<int:pk>/', delete_appointment, name='delete-appointment'),
    path('delete-user/<int:pk>/', delete_user, name='delete-user'),
    path('clear/', clear, name='clear'),
    path('search/', search, name='search'),
    path('inactive_user_clean/', inactive_user_clean, name='inactive_user_clean'),
]


urlpatterns += htmx_patterns