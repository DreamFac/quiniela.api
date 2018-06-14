#!/bin/sh
python manage.py makemigrations api_auth predictor
python manage.py migrate
python manage.py collectstatic  # Collect static files

supervisord

certbot --nginx --non-interactive --agree-tos -m eduardo.avilesj@gmail.com -d a.oraculapp.com