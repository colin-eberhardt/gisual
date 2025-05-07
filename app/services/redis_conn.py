import redis.asyncio as redis
# do some os stuff 

# Create Redis connection 
redis_conn = redis.Redis(host='redis', port=6379, decode_responses=True)