import redis.asyncio as redis

# Create Redis connection 

# Can be more flexible with some config and env vars
redis_conn = redis.Redis(host='redis', port=6379, decode_responses=True)