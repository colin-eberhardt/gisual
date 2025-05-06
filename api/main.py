from fastapi import FastAPI, HTTPException

import api.utils.stations as stations
from api.utils.transform import extract_kml_file, kml_to_dict
from api.utils.distance_calc import haversine_distance

# Create the stations dictionary once at startup
async def lifespan(app: FastAPI):
    # Get KML out of KMZ
    global stations
    kml_path = extract_kml_file("./data/stations.kmz")
    stations.SEPTA_STATIONS = kml_to_dict(kml_path) 
    yield

    # Clean up
    # ml_models.clear()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"stations": stations.SEPTA_STATIONS}

@app.get('/closest/')
def get_closest_station(coords: str):

    # Parse the coords
    request_key = coords.replace(" ", "")
    lat, long = coords.split(",")
    # Find the haversine dist
    haversine_distance((float(lat),float(long)))
    # Return geojson

