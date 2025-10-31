import time
import redis
from fastapi import HTTPException, status

r = redis.Redis(host="localhost", port=6379, db=0)

def throttle_request(user_id: str, limit: int = 5, window: int = 60):
    key = f"throttle:{user_id}"
    current = r.get(key)

    if current and int(current) >= limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Muitas requisições. Tente novamente mais tarde."
        )

    pipe = r.pipeline()
    pipe.incr(key, 1)
    pipe.expire(key, window)
    pipe.execute()

def rate_limit(ip: str, limit: int = 100, window: int = 60):
    key = f"ratelimit:{ip}"
    current = r.get(key)

    if current and int(current) >= limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Limite de requisições atingido."
        )

    pipe = r.pipeline()
    pipe.incr(key, 1)
    pipe.expire(key, window)
    pipe.execute()