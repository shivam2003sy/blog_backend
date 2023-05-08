FROM python:3.9.5

WORKDIR /bloglite

# Install dependencies
RUN apt-get update && \
    apt-get install -y redis-server

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

CMD service redis-server start && python3 run.py --port=5000 && ./local_worker.sh && ./local_beat.sh

