FROM python:3.9-slim

WORKDIR /app

COPY  ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . ./app

COPY data/SEPTARegionalRailStations2016.kmz data/stations.kmz

CMD ["fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]