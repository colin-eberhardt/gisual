from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends
import redis.asyncio as redis

import app.utils.stations as stations
from app.utils.transform import extract_kml_file, kml_to_dict
from app.utils.distance_calc import haversine_distance
from app.utils.cache_utils import get_cached_response, update_cache, create_key
from app.services.redis_conn import redis_conn

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
    request_key = coords.replace(" ", "")
    lat, long = coords.split(",")
    lat, long = float(lat), float(long)

    cache_key = create_key(lat, long)

    # Check the cache
    cached_response = await get_cached_response(cache_key)
    if cached_response:
        return cached_response

    # Find the haversine dist
    closest = haversine_distance((lat,long))
    # Update cache
    await update_cache(cache_key, closest)
    # Return geojson
    return closest

