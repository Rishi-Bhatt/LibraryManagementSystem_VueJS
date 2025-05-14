from celery import Celery
from flask_mail import Message
from flask import render_template
import flask_excel as excel
from datetime import datetime, timedelta
from json import dumps
from httplib2 import Http
from CeleryTasker import FlaskTask
from app import celery_app
from jinja2 import Template

SMTP_HOST = 'localhost'
SMTP_PORT = 1025
SENDER_EMAIL = 'Pustakalay-Librarian@email.com'


def send_email(to, subject, content_body):
    from app import mail  
    msg = Message(subject=subject, recipients=[to], html=content_body)
    mail.send(msg)

# CSV FILE GENERATING TASK
@celery_app.task(base=FlaskTask, ignore_result=False)
def CreateResource_CSV():
    from app import eBooks
    csv_output = None
    ebook_data = eBooks.query.with_entities(eBooks.book_name, eBooks.book_author).all()
    csv_output = excel.make_response_from_query_sets(ebook_data, ['book_name', 'book_author'], "csv")
    filename = 'ebooks.csv'

    with open(filename, 'w') as f:
        if csv_output:
            f.write(csv_output.data)
        else:

            f.write('No data available')

    return filename

# MONTHLY REPORT TASK
@celery_app.task(base=FlaskTask, ignore_result=False)
def MonthlyReport():
    from app import User, Role, Requested, Issued, Feedback, eSection, eBooks
    users = User.query.filter(User.roles.any(Role.name == 'user')).all()

    with open('report.html', 'r') as f:
        template = Template(f.read())
        for user in users:
            requested_books = Requested.query.filter_by(user_id=user.id).all()
            issued_books = Issued.query.filter_by(user_id=user.id).all()
            feedbacks = Feedback.query.filter_by(feedback_user_id=user.id).all()
            sections = eSection.query.all()
            books = eBooks.query.all()
            total_requested_books = len(requested_books)
            total_issued_books = len(issued_books)
            total_logins = user.login_count  

            send_email(user.email, 'Monthly Report', template.render(
                email=user.email, user=user, requested_books=requested_books, issued_books=issued_books, 
                feedbacks=feedbacks, sections=sections, books=books,
                total_requested_books=total_requested_books, total_issued_books=total_issued_books, 
                total_logins=total_logins, report_type='Monthly'))

    return "Monthly Report Sent"

# DAILY REMINDER TASK
@celery_app.task(base=FlaskTask, ignore_result=False)
def DailyReminder():
    from app import User, Role, Requested, Issued, Feedback, eSection, eBooks
    users = User.query.filter(User.roles.any(Role.name == 'user')).all()

    with open('report.html', 'r') as f:
        template = Template(f.read())
        for user in users:
            requested_books = Requested.query.filter_by(user_id=user.id).all()
            issued_books = Issued.query.filter_by(user_id=user.id).all()
            feedbacks = Feedback.query.filter_by(feedback_user_id=user.id).all()
            sections = eSection.query.all()
            books = eBooks.query.all()
            total_requested_books = len(requested_books)
            total_issued_books = len(issued_books)
            total_logins = user.login_count  

            send_email(user.email, 'Daily Reminder', template.render(
                email=user.email, user=user, requested_books=requested_books, issued_books=issued_books, 
                feedbacks=feedbacks, sections=sections, books=books,
                total_requested_books=total_requested_books, total_issued_books=total_issued_books, 
                total_logins=total_logins, report_type='Daily Reminder'))

    return "Daily Reminder Sent"

# REMINDER TO RETURN BOOK TASK
@celery_app.task(base=FlaskTask, ignore_result=False)
def Reminder():
    from app import User, Issued
    users = User.query.all()
    current_time = datetime.utcnow()

    for user in users:
        issued_books = Issued.query.filter_by(user_id=user.id).all()
        for issue in issued_books:
            return_time = issue.return_before
            time_left = return_time - current_time
            hours_left = time_left.total_seconds() // 3600

            if time_left.total_seconds() > 0:
                message = f"Time Remaining to Return the book named {issue.ebooks.book_name} = {hours_left} hours."
            else:
                hours_passed = abs(hours_left)
                fine = hours_passed * 10  
                message = f"{int(hours_passed)} Hours have passed, Kindly return the book as soon as possible, otherwise, a fine of {fine} INR. will be imposed."

            send_email(user.email, f'Return Reminder for {issue.ebooks.book_name} Book', message)

    return "Return Reminders Sent"

# DAILY LOGIN TASK
@celery_app.task(base=FlaskTask, ignore_result=False)
def DailyLogins():
    from app import User
    current_time = datetime.utcnow()

    users = User.query.all()
    for user in users:
        last_login = user.last_login_at
        if last_login:
            time_since_last_login = current_time - last_login
            hours_since_last_login = time_since_last_login.total_seconds() // 3600

            if hours_since_last_login < 24:
                message = f"You have not logged in since {int(hours_since_last_login)} hours. Please Login to Pustakalay to read a variety of books."
            else:
                message = f"{user.username}, you have not used Pustakalay in the last 24 hours! Please login to read our extensive collection of books."

            send_email(user.email, 'Daily Login Reminder', message)

    return "Daily Login Reminders Sent"




## TEST TASKS
@celery_app.task(base=FlaskTask)
def hello_world():
    return "HELLO WORLD"

@celery_app.task(base=FlaskTask)
def mail_test():
    from app import mail  
    email_id = 'test@Pustakalay.com'
    email_subject = 'Test Mail'
    email_body = 'Namaste,\n\nThis is a Test Email.\n Regards,\nPustakalay'

    msg = Message(subject=email_subject, recipients=[email_id], body=email_body)
    mail.send(msg)
    return 'ok'