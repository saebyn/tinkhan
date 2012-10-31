web: gunicorn tinkhan.wsgi -b 0.0.0.0:$PORT
scheduler: python manage.py celeryd -E -B --loglevel=INFO
worker: python manage.py celeryd -E --loglevel=INFO
celerycam: python manage.py celerycam
