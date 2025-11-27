from random import randint
import time
import redis
from django.core.cache import cache


redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def random_code():
    return randint(100_000, 999_999)


def _get_login_key(phone):
    return f"login:{phone}"


#
# def send_sms_code(phone: str, code: int, expire_time=60):
#     print(f"[TEST] Phone: {phone} == Sms code: {code}")
#     _key = _get_login_key(phone)
#     cache.set(_key, code, expire_time)

def send_sms_code(phone: str, code: int, ttl_seconds=60):
    redis_key = f"sms_:{phone}"
    data = redis_client.hgetall(redis_key)
    if data:
        sent_at = float(data.get("sent_at"))
        passed = time.time() - sent_at
        remain = int(ttl_seconds - passed)

        if remain > 0:
            return {
                "allowed": False,
                "remain_seconds": remain
            }
    print(f"[TEST] Phone: {phone}, Code: {code}")
    redis_client.hmset(redis_key, {
        "sent_at": time.time(),
        "code": code
    })
    redis_client.expire(redis_key, ttl_seconds)

    return {
        "allowed": True,
        "remain_seconds": 0
    }


def check_sms_code(phone: str, code: int):
    _key = _get_login_key(phone)
    _code = cache.get(_key)
    print(_code, code)
    return _code == code
