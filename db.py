import redis
import settings
def get_connection():
    return redis.Redis(settings.REDIS_HOST, db=1)