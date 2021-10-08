FROM python:3.7 as pydeps

RUN pip install -U pip && \
    pip install celery==5.1.2

WORKDIR /app/code
COPY tasks.py .
CMD celery -A tasks worker --loglevel=INFO
