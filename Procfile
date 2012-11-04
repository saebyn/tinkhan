web: newrelic-admin run-program gunicorn tinkhan.wsgi -w 10 -b 0.0.0.0:$PORT
scheduler: newrelic-admin run-program python manage.py celeryd -E -B --loglevel=INFO
worker: newrelic-admin run-program python manage.py celeryd -E --loglevel=INFO
celerycam: python manage.py celerycam
