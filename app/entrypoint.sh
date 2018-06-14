#!/bin/sh
python3 manage.py makemigrations api_auth predictor
python3 manage.py migrate
python3 manage.py collectstatic  # Collect static files

supervisord -c /etc/supervisor/conf.d/supervisor-app.conf

certbot --nginx --non-interactive --agree-tos -m eduardo.avilesj@gmail.com -d a.oraculapp.com