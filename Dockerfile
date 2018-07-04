FROM ubuntu:16.04

LABEL maintainer steelcolosus


RUN apt-get update && \
	apt-get upgrade -y && \	
	apt-get install -y \
	python3-pip \
	build-essential libssl-dev libffi-dev python3 python3-dev \
	openssl \
	git \
	nginx \
	supervisor \
	sqlite3 && rm -rf /var/lib/apt/lists/*

RUN apt-get update
RUN apt-get install software-properties-common -y
RUN	add-apt-repository ppa:certbot/certbot -y
RUN	apt-get update
RUN	apt-get install python-certbot-nginx -y


RUN pip3 install --upgrade pip

RUN pip3 install uwsgi

RUN mkdir -p /docker_api/requirements


RUN chmod 777 -R /docker_api

COPY  ./app/requirements /docker_api/requirements

RUN pip3 install -r /docker_api/requirements/production.txt

# setup all the configfiles
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY ./nginx/my_nginx.conf /etc/nginx/sites-available/default
COPY ./nginx/supervisor-app.conf /etc/supervisor/conf.d/

# install uwsgi now because it takes a little while

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE config.settings.production
ENV DJANGO_READ_DOT_ENV_FILE True

WORKDIR /docker_api

COPY  ./app /docker_api

#Static files for django
RUN mkdir -p /docker_api/project/static

#RUN mkdir -p /docker_api/logs

RUN chmod -x entrypoint.sh

RUN chmod -R a+rwX /docker_api
