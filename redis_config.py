import redis
import os
from datetime import timedelta

redis_host = os.getenv("REDIS_HOST", "redis")
redis_port = int(os.getenv("REDIS_PORT", 6379))

jwt_redis_blocklist = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

ACCESS_EXPIRES = timedelta(hours=1)
