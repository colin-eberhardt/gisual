from fastapi import FastAPI, HTTPException
# from contextlib import asynccontextmanager

import api.utils.stations as stations
from api.utils.transform import extract_kml_file, kml_to_dict
from api.utils.distance_calc import haversine_distance

# Create the stations dictionary once at startup
# @asynccontextmanager
async def lifespan(app: FastAPI):
    # Get KML out of KMZ
    global stations
    kml_path = extract_kml_file("./data/stations.kmz")
    stations.SEPTA_STATIONS = kml_to_dict(kml_path) 
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"stations": stations.SEPTA_STATIONS}

@app.get('/station/')
def find_closest_station(coords: str):

    # Parse the coords
    request_key = coords.replace(" ", "")
    lat, long = coords.split(",")
    # Find the haversine dist
    closest = haversine_distance((float(lat),float(long)))
    # Return geojson
    return closest

