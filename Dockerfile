FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y postgresql postgresql-contrib && \
    apt-get clean

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN service postgresql start && \
    su - postgres -c "psql -c \"CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASSWORD}';\"" && \
    su - postgres -c "psql -c \"CREATE DATABASE ${DB_NAME} OWNER ${DB_USER};\""

EXPOSE 5000

CMD service postgresql start && python app.py
