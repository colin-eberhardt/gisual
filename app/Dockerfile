FROM python:3.9-slim

WORKDIR /app

COPY  ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . ./app

COPY data/SEPTARegionalRailStations2016.kmz data/stations.kmz

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]