from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.utils import timezone

from datetime import timedelta

def inactive_user_clean(request):
    # temporary solution until i learn how to use celery.
    users = get_user_model().objects.all()
    for user in users:
        register_time = user.date_joined
        three_hours_ahead = register_time + timedelta(hours=3)
        if three_hours_ahead < timezone.now() and user.is_active == False:
            user.delete()
    return redirect('home')