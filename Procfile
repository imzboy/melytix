web: gunicorn app:app
worker: python celery worker --loglevel=info
celery_beat: python celery beat --loglevel=info
web: venv > .venv; venv PYTHONUNBUFFERED=true honcho start -f Procfile.real 2>&1
