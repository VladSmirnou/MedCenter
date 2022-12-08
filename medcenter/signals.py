from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received

from .models import UserAppointment


@receiver(valid_ipn_received)
def valid_ipn_signal(sender, **kwargs):
    print('Ipn Valid')
    ipn = sender
    if ipn.payment_status == 'Completed':
        order_obj = get_object_or_404(UserAppointment, AppID=ipn.invoice)
        if order_obj.Price == ipn.mc_gross:
            order_obj.paid = True
            order_obj.save()


@receiver(invalid_ipn_received)
def invalid_ipn_signal(sender, **kwargs):
    print('Ipn Invalid')