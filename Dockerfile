FROM python:3.9

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY . /app

ENV FLASK_APP=app.py

CMD ["gunicorn", "--bind", "app:app", "0.0.0.0:8080", "--timeout 120"]
