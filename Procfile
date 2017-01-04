web: gunicorn drftests.wsgi --limit-request-line 8188 --log-file -
worker: celery worker --app=drftests --loglevel=info
