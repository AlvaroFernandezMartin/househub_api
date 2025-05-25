# Usa una imagen oficial de Python
FROM python:3.12-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . /app/

# Instala dependencias
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Recolecta archivos estáticos (si quieres hacerlo aquí)
RUN python manage.py collectstatic --noinput

# Expone el puerto que usará Gunicorn
EXPOSE 8080

# Usa Gunicorn en lugar de runserver
CMD ["gunicorn", "househub_api.wsgi:application", "--bind", "0.0.0.0:8080"]
