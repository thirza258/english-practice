FROM public.ecr.aws/docker/library/python:3.12

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=english_practice.settings \
    DJANGO_DEBUG=0 \
    PORT=5170

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt \
    && python -m nltk.downloader -d /usr/share/nltk_data punkt punkt_tab stopwords \
    && python -m spacy download en_core_web_sm

COPY . /app/
RUN python manage.py collectstatic --noinput

EXPOSE 5170

CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn english_practice.wsgi:application --bind 0.0.0.0:5170 --workers 2 --timeout 120 --access-logfile - --error-logfile -"]
