import os
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse

import app.utils.stations as stations
from app.services.redis_conn import redis_conn
from app.utils.transform import extract_kml_file, convert_kml
from app.utils.distance_calc import haversine_distance
from app.utils.cache_utils import get_cached_response, update_cache, create_key
from app.utils.helpers import validate_coords

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create the stations dictionary once at startup
    global stations
    kml_path = extract_kml_file("./data/stations.kmz")
    stations.SEPTA_STATIONS = convert_kml(kml_path) 

    # Connect to Redis cache. See Explanation.md for Redis comments/thoughts
    try:
        await redis_conn.ping()
        yield
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Unexpected server error. Please try again later."
        )
    finally:
        redis_conn.close()

app = FastAPI(lifespan=lifespan)

@app.get('/station/')
async def find_closest_station(coords: Annotated[str, Query(description="Comma-separated string in form 'latitude, longitude'")]):
    """
        Find the closest SEPTA station to provided latitude and longitude by calculating the Haversine distance between 'coords' and the station coordinates.
    """

    try:
        # Parse the coords and validate
        lat, long = map(float, coords.replace(" ", "").split(","))
        validate_coords(lat, long)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid coordinates. {e}"
        )

    # Create a cache key and lock key
    pid = os.getpid()
    cache_key = create_key(lat, long)
    lock_key = f"lock:{cache_key}"

    # Check the cache
    cached_response = await get_cached_response(cache_key)
    if cached_response:
        return JSONResponse(
            status_code=200,
            content={
                "status": "OK",
                "data": cached_response,
                "detail": "Returned from cache."
            },
            headers={"X-Cache": "HIT", "pid": str(pid)}
        )

    # Acquire and use lock
    lock = redis_conn.lock(lock_key, timeout=10, blocking_timeout=0)
    lock_acquired = await lock.acquire()  

    if not lock_acquired:
        raise HTTPException(status_code=429, detail="A search from your coordinates is already being processed. Try again soon.")

    # If cache missed, find station
    try:
        closest_station = haversine_distance((lat,long))
        # Update cache
        await update_cache(cache_key, closest_station)
        
        # Return the GeoJSON in data
        return JSONResponse(
            status_code=200,
            content={
                "status": "OK",
                "data": closest_station,
                "detail": "Success"
            },
            headers={"X-Cache": "MISS",  "pid": str(pid)}
        )
    finally:
        await lock.release()

