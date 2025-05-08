import json

from app.services.redis_conn import redis_conn

def create_key(lat: str, long:str) -> str:
    # Creates a key for cache

    # Rounding to 5 decimal places since it equatesto ~1m accuracy.
    # https://wiki.openstreetmap.org/wiki/Precision_of_coordinates
    key = f"lat:{round(lat, 5)}:long:{round(long, 5)}"
    return key


async def get_cached_response(key:str):
    # Checks cache for value of giveb key
    response = await redis_conn.get(key)
    return json.loads(response) if response else None


async def update_cache(key:str, station: dict):
    # Creates cache entry for key
    await redis_conn.setex(key, 3600, json.dumps(station))
    print("Cache updated")