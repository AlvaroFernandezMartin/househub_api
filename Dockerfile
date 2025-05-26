FROM python:3.12-slim

WORKDIR /app

COPY . /app/

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

RUN python manage.py migrate --noinput && python manage.py collectstatic --noinput

EXPOSE 8080

CMD ["gunicorn", "househub_api.wsgi:application", "--bind", "0.0.0.0:8080"]
