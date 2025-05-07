from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

import app.utils.stations as stations
from app.services.redis_conn import redis_conn
from app.utils.transform import extract_kml_file, kml_to_dict
from app.utils.distance_calc import haversine_distance
from app.utils.cache_utils import get_cached_response, update_cache, create_key

# Create the stations dictionary once at startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Get KML out of KMZ
    global stations
    kml_path = extract_kml_file("./data/stations.kmz")
    stations.SEPTA_STATIONS = kml_to_dict(kml_path) 

    try:
        await redis_conn.ping()
        print("Connected to Redis instance")
        yield
    except Exception as e:
        print(f"Failed to connect to Redis: {e}")
        raise e
    finally:
        redis_conn.close()

app = FastAPI(lifespan=lifespan)

@app.get('/station/')
async def find_closest_station(coords: str):

    # Parse the coords
    lat, long = coords.replace(" ", "").split(",")
    lat, long = float(lat), float(long)

    cache_key = create_key(lat, long)
    lock_key = f"lock:{cache_key}"

    # Check the cache
    cached_response = await get_cached_response(cache_key)
    if cached_response:
        return cached_response

    # Acquire and use lock
    lock = redis_conn.lock(lock_key, timeout=10, blocking_timeout=0)
    lock_acquired = await lock.acquire()  

    if not lock_acquired:
        raise HTTPException(status_code=429, detail="A search from your coordinates is already being processed. Try again soon.")

    try:
        # Find the haversine dist
        closest = haversine_distance((lat,long))
        # Update cache
        await update_cache(cache_key, closest)
        # Return geojson
        return closest
    finally:
        await lock.release()

