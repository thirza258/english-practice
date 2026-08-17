FROM public.ecr.aws/docker/library/python:3.12

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=english_practice.settings \
    DJANGO_DEBUG=0 \
    PORT=5170

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 5170

CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn english_practice.wsgi:application --bind 0.0.0.0:5170 --workers 2 --access-logfile - --error-logfile -"]
