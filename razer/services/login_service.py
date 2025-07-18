from razer.models import UserAccount
from razer.playwright_client import login_razer_gold
import uuid

def try_login_and_store_session(user: UserAccount) -> bool:
    base_path = "playwright_sessions"
    session_dir = f"{base_path}/{user.id}_{uuid.uuid4().hex[:6]}"

    success = login_razer_gold(
        email=user.email,
        password=user.user_password,
        region_url=user.region.url,
        session_dir=session_dir
    )

    if success:
        user.status = 1  # Online
        user.session_path = session_dir
        user.save()
    return success