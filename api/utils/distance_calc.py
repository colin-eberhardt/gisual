import math

import geojson

import api.utils.stations as stations

# EARTH_CIR = 6371000

def haversine_distance(point: tuple):
    """
        Docstring here
    """
    point_lat, point_long = point 

    point_lat_rad, point_long_rad = math.radians(point_lat), math.radians(point_long)

    min_dist = float('inf')
    closest = {}

    # O(n) where n is len(stations)
    for station in stations.SEPTA_STATIONS:
        
        station_lat_rad, station_long_rad = math.radians(float(station['lat'])), math.radians(float(station['long']))
    
        delta_lat = station_lat_rad - point_lat_rad
        delta_long = station_long_rad - point_long_rad

        hav_dist = math.sin(delta_lat/2)**2 + math.cos(point_lat_rad) * math.cos(station_lat_rad) * math.sin(delta_long/2)**2
        dist = 2 * 6371000 * math.asin(math.sqrt(hav_dist))

        if dist < min_dist:
            min_dist = dist
            closest = station

    station_point = geojson.Point([closest['long'], closest['lat']])
    station_feature = geojson.Feature(geometry=station_point, properties={"line": closest["line"], "station":closest["station"]})

    return station_feature
    