web: gunicorn app:app
main_worker: celery worker --beat --loglevel=info -b redis://h:pf0b2c9e78a670264f0b75b20a33311122bdef5f1d0eae7feca0fc74208319647@ec2-52-48-158-246.eu-west-1.compute.amazonaws.com:23549
