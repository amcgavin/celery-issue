FROM python:3.7 as pydeps

RUN pip install -U pip && \
    pip install git+https://github.com/celery/celery@master

WORKDIR /app/code
COPY tasks.py .
CMD celery -A tasks worker --loglevel=INFO
