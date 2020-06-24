import redis

# Setup our redis connection for storing the blacklisted tokens
revoked_store = redis.StrictRedis(host='localhost', port=6379, db=0,
                                  decode_responses=True)