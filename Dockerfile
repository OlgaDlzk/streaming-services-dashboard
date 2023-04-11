FROM python:3.9

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY . /app

ENV FLASK_APP=app.py

CMD gunicorn app:app -b 0.0.0.0:$PORT
