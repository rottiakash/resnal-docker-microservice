FROM python:3
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt && pip install gunicorn
CMD gunicorn -w 13 --bind unix:resnal.sock -m 777 resanalDjango.wsgi