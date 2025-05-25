FROM python:3.13-slim

WORKDIR /app

RUN python3 -m pip install --upgrade pip

COPY requirements.txt requirements.txt

RUN pip install -r  requirements.txt

COPY . ./app
