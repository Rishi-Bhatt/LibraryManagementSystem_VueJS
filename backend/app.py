from flask import Flask, jsonify
from flask_cors import CORS
from flask_mail import Mail
from flask_restful import Api
from flask_security import Security

from auth_utils import generate_auth_token, hash_password
from config import cache, get_config_class
from models import (
    Feedback,
    Issued,
    Requested,
    Role,
    User,
    db,
    eBooks,
    eSection,
    user_datastore,
)
from resources import register_resources, serve_pdf
from celery_jobs.app_factory import make_celery


def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config_class())

    db.init_app(app)
    api = Api(app)
    CORS(app)

    cache.init_app(app)

    celery = make_celery(app)
    mail = Mail(app)

    return app, api, celery, mail


app, api, celery_app, mail = create_app()

from celery_jobs import tasks


celery_app.conf.update(
    worker_hijack_root_logger=False,
    worker_log_format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    worker_task_log_format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    timezone='Asia/Kolkata',
    enable_utc=False,
)

celery_app.conf.beat_schedule = {
    'send-hello-world': {
        'task': 'celery_jobs.tasks.hello_world',
        'schedule': 5.0,
    },
    'send-test-mail': {
        'task': 'celery_jobs.tasks.mail_test',
        'schedule': 10.0,
    },
    'send-monthly-report': {
        'task': 'celery_jobs.tasks.MonthlyReport',
        'schedule': 20.0,
    },
    'send-daily-reminder': {
        'task': 'celery_jobs.tasks.DailyReminder',
        'schedule': 12.0,
    },
    'send-return-reminder': {
        'task': 'celery_jobs.tasks.Reminder',
        'schedule': 10.0,
    },
    'send-daily-logins': {
        'task': 'celery_jobs.tasks.DailyLogins',
        'schedule': 15.0,
    },
}


@app.get('/hello_world')
def hello_world_view():
    task = tasks.hello_world.delay()
    tasks.mail_test.delay()
    tasks.CreateResource_CSV.delay()
    tasks.MonthlyReport.delay()
    tasks.DailyReminder.delay()
    tasks.Reminder.delay()
    tasks.DailyLogins.delay()
    return jsonify({'task-id': task.id})


@app.route('/pdfs/<filename>')
def serve_pdf_route(filename):
    return serve_pdf(filename)


register_resources(api)
security = Security(app, user_datastore, api)


with app.app_context():
    db.create_all()

    user_datastore.find_or_create_role(name='admin', description='Librarian')
    user_datastore.find_or_create_role(name='user', description='User')
    db.session.commit()

    if not user_datastore.find_user(email='Librarian@Pustakalay.com'):
        admin_user = user_datastore.create_user(
            email='Librarian@Pustakalay.com',
            password=hash_password('admin'),
            username='Librarian',
            authentication_token='',
            roles=['admin', 'user'],
        )
        admin_token = generate_auth_token(admin_user)
        admin_user.authentication_token = admin_token
        db.session.commit()

    if not User.query.filter_by(username='Rishi').first():
        test_user = user_datastore.create_user(
            username='Rishi',
            password=hash_password('rishi'),
            email='Rishi@Pustakalay.com',
            authentication_token='',
            roles=['user'],
        )
        user_token = generate_auth_token(test_user)
        test_user.authentication_token = user_token
        user_datastore.add_role_to_user(test_user, 'user')
        db.session.commit()


if __name__ == '__main__':
    app.run(debug=app.config.get('DEBUG', True), port=5000)
