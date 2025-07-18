from celery import shared_task
from .models import UserAccount
from .services.login_service import try_login_and_store_session
from django_q.tasks import async_task
from .playwright_client import login_razer_gold
from django.core.exceptions import ObjectDoesNotExist
import time
import random


# foe celery
@shared_task
def login_user_account(user_id):
    delay = random.randint(60, 600)  # Wait between 1–10 minutes
    time.sleep(delay)

    try:
        user = UserAccount.objects.get(id=user_id)
        try_login_and_store_session(user)
    except UserAccount.DoesNotExist:
        pass
    

# for django-q2
def login_user_account_async(user_id, *args, retries=None, retry_delay=None, hook=None, **kwargs):
    print("[TASK] login_user_account_async started...")

    try:
        user = UserAccount.objects.get(id=user_id)
    except ObjectDoesNotExist:
        print(f"[!] UserAccount with ID {user_id} does not exist.")
        return

    print(f"[TASK] Logging in user: {user.email}")

    session_dir = f"playwright_sessions/user_{user.id}/"
    success = login_razer_gold(user.email, user.user_password, user.region.url, session_dir)

    print(f"[TASK] Login result: {success}")
    
    if success:
        user.status = 1  # Online
    else:
        user.status = 0  # Offline

    user.session_path = session_dir
    user.save()
    print(f"[TASK] Updated user status to {user.status} and saved session path.")