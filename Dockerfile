FROM python:3.12-slim

WORKDIR /app

COPY . /app/

RUN pip install --upgrade pip && pip install -r requirements.txt

# Ejecutar collectstatic en build
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "househub_api.wsgi:application", "--bind", "0.0.0.0:8000"]
