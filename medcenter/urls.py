from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    home,
    chain_drop,
    user_details,
    user_accounts,
    create_account,
    account_details,
    create_appointment,
    user_appointments,
    delete_appointment,
    transactions,
    clear,
    account_transfer,
    search,
    delete_user,
    SignUpView,
    Login
    )

urlpatterns = [
    path("", home, name='home'),
    path("signup/", SignUpView.as_view(), name='signup'),
    path("login/", Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

htmx_patterns = [
    path('chain-drop/', chain_drop, name='chain-drop'),
    path('user-details/', user_details, name='user-details'),
    path('user-accouts/', user_accounts, name='user-accounts'),
    path('create-account/', create_account, name='create-account'),
    path('account-details/<int:pk>/', account_details, name='account-details'),
    path('create-appointment/', create_appointment, name='create-appointment'),
    path('user-appointments/', user_appointments, name='user-appointments'),
    path('delete-appointment/<int:pk>/', delete_appointment, name='delete-appointment'),
    path('user-transaction/<int:pk>/', transactions, name='user-transaction'),
    path('account-transfer/<int:pk>/', account_transfer, name='account-transfer'),
    path('delete-user/<int:pk>/', delete_user, name='delete-user'),
    path('clear/', clear, name='clear'),
    path('search/', search, name='search'),
]

urlpatterns += htmx_patterns