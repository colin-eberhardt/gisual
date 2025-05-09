# Gisual - SEPTA Station API

This is a preliminary version of a Gisual station-finding application which provides a REST API that allows users to find the SEPTA station nearest their provided coordinate location. At the moment, the SEPTA station dataset is a static KMZ file. 

The application layer is built on top of **FastAPI**. It also includes implementations of **Redis** (for caching and locking), **Nginx** (reverse proxy and rate limiting), and **Gunicorn w/ Uvicorn** for vertical scaling of the application layer. These services have been containerized using **Docker**.

The app is contained within the `/app` directory, wherein you can find the API endpoint(s) in `main.py`, as well as various helpers functions in the `/utils` folder.

Further, there are two functions within `transform.py` which are executed when the FastAPI starts up. These functions are responsible for extracting and transforming the KMZ file into a list of station-specific dicts. 

# Features

- KMZ file extraction and transformation
- Determines nearest station to user input using the Haversin Formula
- Caches responses and acquires locks on searches using Redis
- Rate limits and reverse proxies requests using Nginx
- Vertically scalable via uvicorn workers
- Horizontally scalable via Docker & Gunicorn
- Future-friendly

# Tech Stack

- FastAPI
- Redis
- Nginx
- Gunicorn + Uvicorn
- Docker

# Getting Started

**Assumpton:** You have Docker available on your machine. If not, you'll need to install it: https://www.docker.com/get-started/

1. Clone this repo
2. `cd` into the `gisual` folder on your machine
3. Run `docker compose build`, if running this for the first time.
4. Run `docker compose up -d`

Nice, your app should be available at `http://localhost:8000`

# Usage

GET `/station/` 

**Parameters**

- `coords` (str): This is a comma-separated string in lat, long format. Required. Input validated to ensure string format, and total length not over 50 char. 

**Example**

```
    GET /station/?coords=40, -75
```

**Response**

- JSON reponse wherein the `data` attr contains GeoJSON data for nearest station.

```
    {
        "success":true,
        "data":{
            "type":"Feature",
            "geometry":{
                "type":"Point",
                "coordinates":[-75.345086,40.120847]
            },
            "properties":{
                "line":"Manayunk Norristown Line",
                "station":"Elm Street"
            }
        }
    }
```

**Testing**



**Future Enahncements**