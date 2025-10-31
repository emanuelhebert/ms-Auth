import secrets
import redis
from datetime import datetime, timedelta

r = redis.Redis(host="localhost", port=6379, db=1)

def generate_reset_token(user_id: str, expires_in: int = 900):
    token = secrets.token_urlsafe(32)
    key = f"reset:{token}"
    r.setex(key, expires_in, user_id)
    return token

def validate_reset_token(token: str):
    key = f"reset:{token}"
    user_id = r.get(key)
    if not user_id:
        return None
    return user_id.decode()