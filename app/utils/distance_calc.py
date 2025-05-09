import math
import geojson

import app.utils.stations as stations

EARTH_CIR = 6371000

def haversine_distance(point: tuple) -> dict:
    """
        Calculates the closest distance between a given point and SEPTA stations using the Haversine formaula. 
        Resource: https://en.wikipedia.org/wiki/Haversine_formula

        Parameters:
        -------------
            point: tuple
                The lat and long (lat, long) from which to calculate distance.

        Reponse:
        -------------
            station: dict
                A dict containing station info and geojson data 
                e.g.: {"type":"Feature","geometry":{"type":"Point","coordinates":[-75,40]},"properties":{"line":"Manayunk Norristown Line","station":"Elm Street"}}
    """
    point_lat_rad, point_long_rad = math.radians(point[0]), math.radians(point[1])

    min_dist = float('inf')
    closest_station = {}

    # O(n) where n is len(stations)
    for station in stations.SEPTA_STATIONS:
        
        station_lat_rad, station_long_rad = math.radians(station['lat']), math.radians(station['long'])
    
        delta_lat = station_lat_rad - point_lat_rad
        delta_long = station_long_rad - point_long_rad

        # Haversin Formula
        hav_dist = math.sin(delta_lat/2)**2 + math.cos(point_lat_rad) * math.cos(station_lat_rad) * math.sin(delta_long/2)**2
        dist = 2 * EARTH_CIR * math.asin(math.sqrt(hav_dist))

        # If closest, set trackers
        if dist < min_dist:
            min_dist = dist
            closest = station

    # Convert to geojson
    station_point = geojson.Point([closest['long'], closest['lat']])
    station_feature = geojson.Feature(geometry=station_point, properties={"line": closest["line"], "station":closest["station"]})

    return station_feature
    