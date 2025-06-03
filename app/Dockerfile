# FROM python:3.13-slim AS builder
#
# WORKDIR /app
# # Prevents Python from writing .pyc files to disk
# ENV PYTHONDONTWRITEBYTECODE=1
# # Ensures Python output is sent straight to terminal without buffering
# ENV PYTHONUNBUFFERED=1
# RUN pip install --upgrade pip
# # Install system dependencies:
# # libpq-dev: Required for psycopg2 (PostgreSQL adapter)
# # gcc: Required for compiling some Python packages
# RUN apt-get update \
#     && apt-get -y install libpq-dev gcc
# COPY app/requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
# COPY app/ .
# EXPOSE 8000
# RUN chmod +x  /app/entrypoint.prod.sh
# CMD ["/app/entrypoint.prod.sh"]

########################################################

###########
# BUILDER #
###########

# pull official base image
FROM python:3.11.4-slim-buster as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

COPY ./ /usr/src/app/
# lint
RUN pip install --upgrade pip
# RUN pip install flake8==6.0.0
# RUN flake8 --ignore=E501,F401 .

# install python dependencies
# COPY ./requirements.txt .
# RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt
RUN pip install -r requirements.txt


#########
# FINAL #
#########

# pull official base image
FROM python:3.11.4-slim-buster

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup --system app && adduser --system --group app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME
COPY ./ $APP_HOME

# install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends netcat
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.sh
RUN chmod +x  $APP_HOME/entrypoint.sh

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

# run entrypoint.prod.sh
ENTRYPOINT ["/home/app/web/entrypoint.sh"]