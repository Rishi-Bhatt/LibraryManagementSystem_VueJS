# CeleryTasker.py

from celery import Celery, Task


def make_celery(app) -> Celery:
    celery = Celery(app.import_name)
    celery.config_from_object('CeleryConfig')
    # celery.Task = FlaskTask
    return celery



