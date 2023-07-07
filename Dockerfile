FROM python:3.11-alpine3.16
WORKDIR /app
COPY . /app
EXPOSE 8000
RUN apk add postgresql-client build-base postgresql-dev
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENV PYTHONUNBUFFERED=1
RUN adduser --disabled-password rental
USER rental
