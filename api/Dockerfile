FROM python:3.9-slim

WORKDIR /app

COPY  ./requirements.txt /api/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /api/requirements.txt

COPY . ./api

COPY data/SEPTARegionalRailStations2016.kmz data/stations.kmz

CMD ["fastapi", "run", "api/main.py", "--host", "0.0.0.0", "--port", "8000"]