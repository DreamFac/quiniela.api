FROM python:3.6.2

LABEL maintainer steelcolosus


RUN apt-get update && \
	apt-get upgrade -y && \	
	apt-get install -y \
	git \
	nginx \
	supervisor \
	sqlite3 && \
	rm -rf /var/lib/apt/lists/*


#RUN apt-get install software-properties-common && \
#	add-apt-repository ppa:certbot/certbot && \
#	apt-get update && \
#	apt-get install python-certbot-nginx 


RUN pip install --upgrade pip

RUN pip install uwsgi

RUN mkdir -p /docker_api/requirements


RUN chmod 777 -R /docker_api

COPY  ./app/requirements /docker_api/requirements

RUN pip install -r /docker_api/requirements/production.txt
# setup all the configfiles
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY ./nginx/my_nginx.conf /etc/nginx/sites-available/default
COPY ./nginx/supervisor-app.conf /etc/supervisor/conf.d/


#installing nginx https certificate
#RUN sudo certbot --nginx

# install uwsgi now because it takes a little while

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE config.settings.production
ENV DJANGO_READ_DOT_ENV_FILE True

WORKDIR /docker_api

COPY  ./app /docker_api

#Static files for django
RUN mkdir -p /docker_api/project/static

RUN chmod -x entrypoint.sh

RUN chmod -R a+rwX /docker_api
