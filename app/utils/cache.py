import redis
from flask import app

def get_cache():
    """ Returns the Redis cache connection """
    return redis.StrictRedis.from_url(app.config['REDIS_URL'])

def set_cache(key, value, ttl=3600):
    """ Sets a value in Redis cache with optional TTL """
    cache = get_cache()
    cache.setex(key, ttl, value)

def get_cache_value(key):
    """ Retrieves a value from Redis cache """
    cache = get_cache()
    return cache.get(key)
