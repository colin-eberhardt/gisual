import json

from app.services.redis_conn import redis_conn

def create_key(lat: str, long:str) -> str:
    # 5 decimal places --> ~1m accuracy
    key = f"lat:{round(lat, 5)}:long:{round(long, 5)}"
    return key


async def get_cached_response(key:str):
    response = await redis_conn.get(key)
    return json.loads(response) if response else None


async def update_cache(key:str, station: dict):
    await redis_conn.setex(key, 3600, json.dumps(station))
    print("Cache updated")