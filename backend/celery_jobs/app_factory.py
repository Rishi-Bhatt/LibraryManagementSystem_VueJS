from celery import Celery


def make_celery(app) -> Celery:
    celery = Celery(app.import_name)
    celery.config_from_object('celery_jobs.config')
    return celery
