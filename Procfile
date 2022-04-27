web: gunicorn --pythonpath Buyabook Buyabook.wsgi
release: python manage.py migrate
release: python manage.py loaddata groups