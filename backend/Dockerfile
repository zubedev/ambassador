FROM python:3.9
MAINTAINER zube.dev

ENV PYTHONUNBUFFERED 1

WORKDIR /backend
COPY . /backend

RUN pip install -r requirements.txt

CMD python manage.py wait_for_database && \
    python manage.py migrate --noinput && \
    python manage.py runserver 0.0.0.0:8000
