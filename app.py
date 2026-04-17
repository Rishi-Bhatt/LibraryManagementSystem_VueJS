from flask import Flask, current_app, jsonify, make_response, request, send_from_directory, send_file
from flask_security import Security, SQLAlchemyUserDatastore, current_user, roles_accepted, auth_token_required, verify_password, login_user
from config import DevConfig
from flask_restful import Api
from flask_restful import Resource
from flask_cors import CORS
import bcrypt
from functools import wraps
from sqlalchemy.exc import SQLAlchemyError
import os
import time
from werkzeug.utils import secure_filename
import razorpay

from io import BytesIO
from caching import cache
from celery import Celery, shared_task
from worker import make_celery
from flask_mail import Mail


from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask_security import UserMixin, RoleMixin, AsaList, SQLAlchemyUserDatastore
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import Boolean, or_ , DateTime, Column, Float,  Integer, \
                    String, ForeignKey




db = SQLAlchemy()
def create_app():
    
    app = Flask(__name__)
    app.config.from_object(DevConfig)
    
    db.init_app(app)
    api = Api(app)
    CORS(app)

    cache.init_app(app)

    celery = make_celery(app)
    
    mail = Mail(app)
    # mail.init_app(app)
    
    return app, api, celery, mail


app, api, celery_app, mail = create_app()


import tasks

# Beat Schedule Configuration
from celery.schedules import crontab
celery_app.conf.update(
    worker_hijack_root_logger=False,
    worker_log_format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    worker_task_log_format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    timezone='Asia/Kolkata',
    enable_utc=False)

celery_app.conf.beat_schedule = {
    
        'send-hello-world': {
            'task': 'tasks.hello_world',
            'schedule': 5.0
        },
        'send-test-mail': {
            'task': 'tasks.mail_test',
            'schedule': 10.0
        },
        'send-monthly-report': {
            'task': 'tasks.MonthlyReport',
            'schedule': 20.0 #crontab(day_of_month=1, hour=8, minute=30), 
        },
        'send-daily-reminder': {
            'task': 'tasks.DailyReminder',
            'schedule': 12.0 #crontab(minute=0, hour=0),  # Every day at midnight
        },
        'send-return-reminder': {
            'task': 'tasks.Reminder',
            'schedule': 10.0 #crontab(minute=0, hour=9),  # Every day at 9 AM
        },
        'send-daily-logins': {
            'task': 'tasks.DailyLogins',
            'schedule': 15.0 #crontab(minute=0, hour=10),  # Every day at 10 AM
        }
    }




import tasks

@app.get('/hello_world')
def hello_world_view():
    t = tasks.hello_world.delay()
    tasks.mail_test.delay()
    tasks.CreateResource_CSV.delay()
    tasks.MonthlyReport.delay()
    tasks.DailyReminder.delay()
    tasks.Reminder.delay()
    tasks.DailyLogins.delay()
    return jsonify({"task-id" : t.id})




def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(hashed_password, password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))




#======================================================================================================
#======================================================================================================
#===========================  DATABASE MODELS  ========================================================
#======================================================================================================
#======================================================================================================


class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))



class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))
    permissions = Column(MutableList.as_mutable(AsaList()), nullable=True)



class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255), unique=True, nullable=True)
    password = Column(String(255), nullable=False)
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    active = Column(Boolean())
    fs_uniquifier = Column(String(64), unique=True, nullable=False)
    confirmed_at = Column(DateTime())
    authentication_token = db.Column(db.String(255))
    roles = relationship('Role', secondary='roles_users',
                         backref=backref('users', lazy='dynamic'))
    
    def get_auth_token(self):
        s =  URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        token = s.dumps({'id': self.id})
        self.authentication_token = token
        db.session.commit()
        print("Token Updated Successfully")
        return token





class eSection(db.Model):
    __tablename__ = "eSection"
    section_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    section_name = db.Column(db.String(500), nullable = False)
    description = db.Column(db.String(2000), nullable = False)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.now())
    created_by = db.Column(db.String(255), db.ForeignKey('user.id'))
    updated_by = db.Column(db.String(255), db.ForeignKey('user.id'), default=None)
    updated_at = db.Column(db.DateTime, default = None)
    ebooks = db.relationship('eBooks', back_populates='esection', lazy=True)
    status = db.Column(db.Boolean)
    def __repr__(self) -> str:
         return f"{self.section_name}"



class eBooks(db.Model):
    __tablename__ = "eBooks"
    book_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    book_name = db.Column(db.String(255), nullable = False)
    book_author = db.Column(db.String(255), nullable = False)
    book_content = db.Column(db.LargeBinary, nullable = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.now())
    dateissued = db.Column(db.DateTime, nullable = True, default = None)
    returndate = db.Column(db.DateTime, nullable = True, default = None)
    created_by = db.Column(db.String(255), db.ForeignKey('user.id'))
    updated_by = db.Column(db.String(255), db.ForeignKey('user.id'), default=None)
    updated_at = db.Column(db.DateTime, default = None)
    sectionid = db.Column(db.Integer, db.ForeignKey('eSection.section_id'))
    esection = db.relationship('eSection', back_populates='ebooks', lazy=True)
    requested = db.relationship('Requested', back_populates='ebooks', lazy=True)
    issued = db.relationship('Issued', back_populates='ebooks', lazy=True, foreign_keys='Issued.bookid')
    status = db.Column(db.Boolean, default=True)
    DownloadPrice = db.Column(db.Float, nullable=False)
    
    def __repr__(self) -> str:
         return f"{self.book_name}"




class Requested(db.Model):
    __tablename__ = 'requested'
    request_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255), db.ForeignKey('user.id'))
    bookid = db.Column(db.Integer, db.ForeignKey('eBooks.book_id'))
    requested_at = db.Column(db.DateTime, default=None)
    user = db.relationship('User', backref=db.backref('requested_books', lazy=True))
    ebooks = db.relationship('eBooks', back_populates='requested', lazy=True, foreign_keys=[bookid])
    status = db.Column(db.String(255), default='Pending')
    def __repr__(self) -> str:
         return f"{self.request_id}"



class Issued(db.Model):
    __tablename__ = 'issued'
    issue_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    bookid = db.Column(db.Integer, db.ForeignKey('eBooks.book_id'))
    user = db.relationship('User', backref=db.backref('issued_books', lazy=True))
    ebooks = db.relationship('eBooks', back_populates='issued', lazy=True, foreign_keys=[bookid])
    issued_at = db.Column(db.DateTime)
    return_before = db.Column(db.DateTime)
    status = db.Column(db.String(50), default='Issued') #Overdue
    def __repr__(self) -> str:
         return f"{self.issue_id}"



class Feedback(db.Model):
    __tablename__ = 'feedback'
    name = db.Column(db.String(200), nullable = False)
    email = db.Column(db.String(500), nullable = False)
    feedback_message = db.Column(db.String(2000), nullable = False)
    rating_id = db.Column(Integer, primary_key=True, autoincrement=True)
    feedback_user_id = Column(Integer, ForeignKey('user.id'), nullable=False) 
    book_id = Column(Integer, ForeignKey('eBooks.book_id'), nullable=False)  
    rating_value = db.Column(Float, nullable=False)  # Rating given
    feedback_time = Column(DateTime, default=datetime.now, nullable=False)  

    def __repr__(self) -> str:
         return f"Rating({self.rating_id}, Rater: {self.feedback_user_id}, Book: {self.book_id}, Rating: {self.rating_value})"

    




user_datastore = SQLAlchemyUserDatastore(db,User,Role)



def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        print(auth_header)
        if auth_header:
            token = auth_header.split(" ")[1]  # Assuming the token is in the format "Bearer <token>"
            print(token)
            user = user_datastore.find_user(authentication_token=token)
            print(user)
            if user:
                login_user(user)
                print("login_user(user)")
            else:
                print("Invalid or expired token, 401")
                return jsonify({"message": "Invalid or expired token"}), 401
        else:
            print("Token missing, 403")
            return jsonify({"message": "Token is missing"}), 403
        
        return f(*args, **kwargs)
    
    return decorated




#======================================================================================================
#======================================================================================================
#==============================  LOGIN AND REGISTER API'S  ============================================
#======================================================================================================
#======================================================================================================



class User_Login(Resource):

    def post(self):
        print("POST REQ RECEIVED")
        data = request.get_json()
        email = data['email']
        password = data['password']
        user = user_datastore.find_user(email = email)
        if user:
            if check_password(user.password, password):
                login_user(user)
                token = user.get_auth_token()
                
                db.session.commit()
               
                
                role = 'admin' if current_user.has_role('admin') else 'user'
                
                return make_response(jsonify({
                    'token': token, 
                    'email': user.email,
                    'id': user.id,
                    'role': role,
                    'username': user.username,
                    'message': 'Login Successful'
                }), 200)
            return make_response(jsonify({"message" : "Wrong Password", "password" : check_password(user.password, password) }), 401)
        return make_response(jsonify({"message" : "Incorrect Email", "email" : email }), 404)
    
    def options(self, *args, **kwargs):
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        return response




class Librarian_Login(Resource):

    def post(self):
        print("POST REQ RECEIVED")
        data = request.get_json()
        email = data['email']
        password = data['password']
        user = user_datastore.find_user(email = email)

        if user:
            if check_password(user.password, password):
                login_user(user)
                token = user.get_auth_token()
                
                db.session.commit()
                
                role = 'admin' if current_user.has_role('admin') else 'user'
                return make_response(jsonify({
                    'token': token, 
                    'email': user.email,
                    'id': user.id,
                    'role': role,
                    'username': user.username,
                    'message': 'Login Successful'
                }), 200)
            return make_response(jsonify({"message" : "Wrong Password", "password" : check_password(user.password, password) }), 401)
        return make_response(jsonify({"message" : "Incorrect Email", "email" : email }), 404)


    def options(self, *args, **kwargs):
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        return response
    

    
   

class register(Resource):
    def post(self):
        print("POST REQ RECEIVED")
        data = request.get_json()
        email = data['email']
        password = data['password']
        username = data['username']
        if not email:
            return make_response(jsonify({"message" : "Email required"}), 400)
        if not password:
            return make_response(jsonify({"message" : "Password required"}), 400)
        if not username:
            return make_response(jsonify({"message" : "Username required"}), 400)
        
        user_check_email = user_datastore.find_user(email = email)
        user_check_username = user_datastore.find_user(username = username)
        if user_check_email:
            return make_response(jsonify({"message" : "User Email already present"}), 400)
        if user_check_username:
            return make_response(jsonify({"message" : "Username already present"}), 400)
        
        hashed_password = hash_password(password)
        
        user = user_datastore.create_user(email=email, password = hashed_password, username=username)

        user_datastore.add_role_to_user(user, 'user')
        db.session.commit()
        return make_response(jsonify({'message' : "User registered successfully",'username' : user.username, 'email' : user.email}),201)


    def options(self, *args, **kwargs):
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        return response



#======================================================================================================
#======================================================================================================
#==============================  ESECTION API'S  ======================================================
#======================================================================================================
#======================================================================================================


class EsectionResource(Resource):
    @token_required
    @roles_accepted('admin', 'user')
    @cache.cached(timeout=1)
    def get(self):
        search_query = request.args.get('search', '')
        print("GET REQ RECEIVED")
        
        query = db.session.query(eSection)
        if search_query:
            query = query.filter(
                or_(
                    eSection.section_name.ilike(f'%{search_query}%'),
                    eSection.description.ilike(f'%{search_query}%')
                )
            )

        ES = query.all()
        data = []
        for es in ES:
            eS = {
                "section_id" : es.section_id,
                "section_name" : es.section_name,
                "date_created" : es.date_created.isoformat(),
                "description" : es.description,
                "created_by" : es.created_by,
                "updated_by" : es.updated_by,
                "updated_at" : es.updated_at.isoformat() if es.updated_at else None,
            }
            data.append(eS)
        
        if not data:
            return make_response(jsonify({"message" : "No Sections Found"}), 404)
        return make_response(jsonify({"message" : "Get All Sections", "data": data}), 200)


    
    @token_required
    @roles_accepted('admin')
    def post(self):
        print("POST REQ RECEIVED")
        print(f"Current user roles: {current_user.roles}")
        auth_header = request.headers.get('Authorization')
        if auth_header:
            token = auth_header.split(" ")[1]  
            print(f"Received token: {token}")
        else:
            print("No token received")
        if not current_user.is_authenticated :
            print("User not authenticated")
        if not current_user.is_active :
            print("User not active")
        if current_user.is_anonymous :
            print("User is anonymous")
            return make_response(jsonify({"message" : "User is anonymous"}), 400)
        data = request.get_json()
        section_name = data['section_name']
        if not section_name:
            return make_response(jsonify({"message" : "Name required"}), 400)
        description = data['description']
        if not description:
            return make_response(jsonify({"message" : "Description required"}), 400)

        es = eSection(
            section_name=section_name, 
            description=description, 
            status=True if current_user.has_role('admin') else False, 
            date_created=datetime.now(), 
            created_by=current_user.id
        )
        db.session.add(es)
        db.session.commit()
        return make_response(jsonify({
            "message": "E-Book_Section Created Successfully", 
            "section_id": es.section_id,  
            "section_name": es.section_name, 
            "status": es.status 
        }), 201)

    def options(self, *args, **kwargs):
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        return response







class EsectionSpecific(Resource):
    
    @token_required
    @roles_accepted('admin', 'user')
    @cache.cached(timeout=1)
    def get(self, section_id):
        print("ESECTION SPECIFIC GET REQUEST RECEIVED")
        ES = eSection.query.filter_by(section_id=section_id).first()
        if not ES:
            return make_response(jsonify({"message" : "Section with this id not found"}), 404)
        ES = {
            "section_id" : ES.section_id,
            "section_name" : ES.section_name,
            "date_created" : ES.date_created.isoformat(),
            "description" : ES.description,
            "created_by" : ES.created_by,
            "updated_by" : ES.updated_by,
            "updated_at" : ES.vitem.updated_at.isoformat() if ES.updated_at else None,
        }
        return make_response(jsonify({"message" : "Found Section with this id", "data": ES}), 200)
    
    
    @token_required
    @roles_accepted('admin')
    def put(self, section_id):
        print("PUT REQUEST RECEIVED")
        try : 
            ES = eSection.query.filter_by(section_id=section_id).first()
            print(ES)
            if not ES:
                return make_response(jsonify({"message" : "Section with this id not found"}), 404)
            data = request.get_json()
            section_name = data['section_name']
            print(section_name)
            if not section_name:
                return make_response(jsonify({"message" : "Name required"}), 400)
            description = data['description']
            print(description)
            if not description:
                return make_response(jsonify({"message" : "Description required"}), 400)
            
            print(ES.section_name)
            ES.section_name = section_name
            print("Updated name", section_name)
            print(ES.description)
            ES.description = description
            print("Updated description", description)
            ES.updated_at = datetime.now()
            print("Updated updated_at")
            ES.updated_by = current_user.id
            print("Updated updated_by")
            if current_user.has_role('admin'):
                ES.status = True
            else:
                ES.status = False
            db.session.commit()
            print("Database committed")
            return make_response(jsonify({"message" : "Updated", "section_id": section_id}), 200)
        
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"message": "Error updating section", "error": str(e)}), 500
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Unexpected error", "error": str(e)}), 500



    @token_required
    @roles_accepted('admin')
    def delete(self, section_id):
        print("DELETE REQUEST RECEIVED")
        ES = eSection.query.filter_by(section_id=section_id).first()
        if not ES:
            return make_response(jsonify({"message" : "No eSection found by that id"}), 404)

        eBooks_in_section = eBooks.query.filter_by(sectionid=section_id).all()
        if eBooks_in_section:
            return make_response(jsonify({"message" : "Cannot delete eSection as it contains eBooks"}), 400)

        db.session.delete(ES)
        db.session.commit()
        return jsonify({"message" : "Deleted Specific eSection", "section_id" : section_id})


    def options(self, *args, **kwargs):
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        return response


@app.route('/pdfs/<filename>')
def serve_pdf(filename):
    return send_from_directory(os.path.join(current_app.instance_path), filename)



#======================================================================================================
#======================================================================================================
#=================================  EBOOK API'S  ======================================================
#======================================================================================================
#======================================================================================================


class EbooksResource(Resource):
    @token_required
    @roles_accepted('admin')
    def post(self):
        sectionname = ''
        print("POST REQ RECEIVED")
        print("POST REQ RECEIVED")
        print(f"Current user roles: {current_user.roles}")
        auth_header = request.headers.get('Authorization')
        if auth_header:
            token = auth_header.split(" ")[1]  
            print(f"Received token: {token}")
        else:
            print("No token received")
        if not current_user.is_authenticated :
            print("User not authenticated")
        if not current_user.is_active :
            print("User not active")
        if current_user.is_anonymous :
            print("User is anonymous")
            return make_response(jsonify({"message" : "User is anonymous"}), 400)
        
        book_name = request.form.get('book_name')
        if not book_name:
            return make_response(jsonify({"message": "Book name is required"}), 400)
        
        book_author = request.form.get('book_author')
        if not book_author:
            return make_response(jsonify({"message": "Book Author is required"}), 400)
        
        DownloadPrice = request.form.get('DownloadPrice')
        if not DownloadPrice:
            return make_response(jsonify({"message": "Please Decide Download Price"}), 400)
        
        sectionid = request.form.get('section_id')
        if not sectionid:
            return make_response(jsonify({"message": "Section ID not found"}), 400)
        
        sectionname = request.form.get('section_name')
        print(sectionname)
        
        if 'book_content' not in request.files:
            return make_response(jsonify({"message": "No file part"}), 400)
        
        book_content = request.files['book_content']
        if book_content.filename == '':
            return make_response(jsonify({"message": "No selected file"}), 400)
        
        ebook = eBooks(
            book_name=book_name,
            book_author=book_author,
            DownloadPrice=DownloadPrice,
            sectionid=sectionid,
            book_content=book_content.read(),  
            created_by=current_user.id,
            date_created=datetime.now()
        )
        db.session.add(ebook)
        db.session.commit()
        
        book_id = ebook.book_id
        filename = f"{book_id}.pdf"
        pdf_path = os.path.join(current_app.instance_path, filename)
        print(pdf_path)
        
        book_content.seek(0)
        book_content.save(pdf_path)
        
        return make_response(jsonify({"message": "eBook Created Successfully", "book_id": ebook.book_id, "book_name": ebook.book_name}), 201)



    @token_required
    @roles_accepted('admin', 'user')
    @cache.cached(timeout=1)
    def get(self):
        search_query = request.args.get('search', '')
        query = db.session.query(eBooks)
        if search_query:
            query = query.filter(
                or_(
                    eBooks.book_name.ilike(f'%{search_query}%'),
                    eBooks.book_author.ilike(f'%{search_query}%')
                )
            )
        
        eb = query.all()
        EBdata = []
        for ebook in eb:
            EB = {
                'book_id': ebook.book_id,
                'book_name': ebook.book_name,
                'book_author': ebook.book_author,
                'DownloadPrice': ebook.DownloadPrice,
                'status': ebook.status,
                'sectionid': ebook.sectionid,
                'created_by': ebook.created_by,
                'updated_by': ebook.updated_by,
                'date_created': ebook.date_created.isoformat(),
                'updated_at': ebook.updated_at.isoformat() if ebook.updated_at else None,
            }
            EBdata.append(EB)

        if not EBdata:
            return make_response(jsonify({"message": "No eBook Found"}), 404)
        return make_response(jsonify({"message": "Get all eBooks", "EBdata": EBdata}), 200)
    
    
    
    
    
    
    def options(self, *args, **kwargs):
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        return response



class EbooksSpecific(Resource):
    @token_required
    @roles_accepted('admin', 'user')
    @cache.cached(timeout=1)
    def get(self, book_id):
        ebook = eBooks.query.filter_by(book_id=book_id).first()
        if not ebook:
            return make_response(jsonify({"message": "No eBook found by that id"}), 404)
        
        data = {
            'book_id': ebook.book_id,
            'book_name': ebook.book_name,
            'book_author': ebook.book_author,
            'DownloadPrice': ebook.DownloadPrice,
            'status': ebook.status,
            'sectionid': ebook.sectionid,
            'created_by': ebook.created_by,
            'updated_by': ebook.updated_by,
            'date_created': ebook.date_created.isoformat(),
            'updated_at': ebook.updated_at.isoformat() if ebook.updated_at else None,
            
        }
        return jsonify({"message": "Get specific eBook", "data": data})



    @token_required
    @roles_accepted('admin')
    def put(self, book_id):
        eb = eBooks.query.filter_by(book_id=book_id).first()
        if not eb:
            return make_response(jsonify({"message": "No eBook found by that id"}), 404)
        
        book_name = request.form.get('book_name')
        book_author = request.form.get('book_author')
        DownloadPrice = request.form.get('DownloadPrice')
        
        
        if not book_name:
            return make_response(jsonify({"message": "Book name is required"}), 400)
        elif not book_author:
            return make_response(jsonify({"message": "Book author is required"}), 400)
        elif not DownloadPrice:
            return make_response(jsonify({"message": "Download price must be specified"}), 400)
        else:
            
            if 'book_content' in request.files:
                book_content = request.files['book_content']
                if book_content.filename == '':
                    return make_response(jsonify({"message": "No file selected"}), 400)

                file_content = book_content.read()
                if not file_content:
                    return make_response(jsonify({"message": "File content is empty"}), 400)

                filename = f"{book_id}.pdf"
                pdf_path = os.path.join(current_app.instance_path, filename)

                book_content.seek(0)
                book_content.save(pdf_path)

                eb.book_content = file_content

            eb.book_name = book_name
            eb.book_author = book_author
            eb.DownloadPrice = DownloadPrice
            eb.updated_at = datetime.now()
            eb.updated_by = current_user.id

        try:
            db.session.commit()
            return make_response(jsonify({"message": "Book updated successfully", 'book_id': book_id}), 200)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"message": "Failed to update the book", "error": str(e)}), 500)
    
    
    
    
    @token_required
    @roles_accepted('admin')
    def delete(self, book_id):
        eb = eBooks.query.filter_by(book_id=book_id).first()
        if not eb:
            return make_response(jsonify({"message": "No eBook found by that id"}), 404)
        
        issued_entry = Issued.query.filter_by(bookid=book_id).first()
        if issued_entry:
            user = User.query.filter_by(id=issued_entry.user_id).first()
            return make_response(jsonify({"message": f"This eBook is currently issued by {user.username} and cannot be deleted"}), 400)
        
        db.session.delete(eb)
        db.session.commit()
        return jsonify({"message": "Deleted specific eBook", 'book_id': book_id})
    
    
    

    def options(self, *args, **kwargs):
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        return response
    
    
    
#======================================================================================================
#======================================================================================================
#==============================  API FOR EBOOK READ AND DOWNLOAD  =====================================
#======================================================================================================
#======================================================================================================


class Ebooks_Download_PDF_API(Resource):
    
    def get(self, book_id):
        ebook = eBooks.query.filter_by(book_id=book_id).first()
        if not ebook:
            return jsonify({"message": "No eBook found by that id"}), 404

        if not ebook.book_content:
            return jsonify({"message": "No content available for this book"}), 404

        # try:
        # Create a file-like object from the book content
        file_stream = BytesIO(ebook.book_content)
        print(file_stream)
        # Send the file to the client
        return make_response(send_file(
            file_stream,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'{ebook.book_name}.pdf'
        ))

        
        
        
        
class Ebooks_Read_PDF_API(Resource):
    
    def get(self, book_id):
        ebook = eBooks.query.filter_by(book_id=book_id).first()
        if not ebook:
            return jsonify({"message": "No eBook found by that id"}), 404

        if not ebook.book_content:
            return jsonify({"message": "No content available for this book"}), 404

        file_stream = BytesIO(ebook.book_content)
        print(file_stream)

        return make_response(send_file(
            file_stream,
            mimetype='application/pdf',
            as_attachment=False,
        ))





#======================================================================================================
#======================================================================================================
#==============================  API FOR REQUESTED EBOOKS  ============================================
#======================================================================================================
#======================================================================================================
    
    
    
class RequestAPI(Resource):
    
    @token_required
    @roles_accepted('admin', 'user')
    @cache.cached(timeout=1)
    def get(self):
        user_id = request.args.get('user_id')
        search_query = request.args.get('search', '')  

        if not user_id:
            return make_response(jsonify({'error': 'User ID is required'}), 400)

        try:
            query = db.session.query(
                Requested,
                eBooks.book_name,
                eBooks.book_author,
                eSection.section_name,
                User.username
            ).join(eBooks, Requested.bookid == eBooks.book_id)\
            .join(eSection, eBooks.sectionid == eSection.section_id)\
            .join(User, Requested.user_id == User.id)\
            .filter(Requested.user_id == user_id)

            if search_query:
                query = query.filter(
                    or_(
                        eBooks.book_name.ilike(f'%{search_query}%'),
                        eBooks.book_author.ilike(f'%{search_query}%'),
                        eSection.section_name.ilike(f'%{search_query}%')
                    )
                )

            requested_books = query.all()
            data = [
                {
                    'username': req[4],
                    'book_name': req[1],
                    'book_author': req[2],
                    'section_name': req[3],
                    'requested_at': req[0].requested_at.isoformat() if req[0].requested_at else 'N/A',
                    'status': req[0].status
                }
                for req in requested_books
            ]

            return make_response(jsonify({"message": "get all requests", "data": data}), 200)

        except Exception as e:
            print(e)
            return make_response(jsonify({'error': 'An error occurred while fetching requests'}), 500)
    
    
    @token_required
    @roles_accepted('admin', 'user')
    def post(self):
        user_id = request.json.get('user_id')
        bookid = request.json.get('bookid')

        if not user_id or not bookid:
            return make_response(jsonify({'error': 'User ID and Book ID are required'}), 400)

        book = db.session.query(eBooks).filter_by(book_id=bookid).first()
        if not book:
            return make_response(jsonify({'error': 'Book not found'}), 404)

        issued_book = db.session.query(Issued).filter_by(bookid=bookid).first()
        if issued_book:
            issued_by_user = db.session.query(User).filter_by(id=issued_book.user_id).first()
            return make_response(jsonify({'error': f'Book already issued by {issued_by_user.username}'}), 400)

        same_user_request = db.session.query(Requested).filter_by(user_id=user_id, bookid=bookid).first()
        if same_user_request:
            return make_response(jsonify({'error': 'Book already requested by you'}), 400)

        existing_request = db.session.query(Requested).filter_by(bookid=bookid).first()
        warning_message = None
        if existing_request and existing_request.user_id != user_id:
            requested_by_user = db.session.query(User).filter_by(id=existing_request.user_id).first()
            warning_message = f'This book is already requested by {requested_by_user.username}, chances of your request getting approved are less, since requests are approved on a first come first serve basis.'

        issued_books_count = db.session.query(Issued).filter_by(user_id=user_id).count()
        requested_books_count = db.session.query(Requested).filter_by(user_id=user_id).count()
        total_books = issued_books_count + requested_books_count

        if total_books >= 5:
            return make_response(jsonify({'error': 'You cannot request more than 5 books. Please return some books to make new requests.'}), 400)

        remaining_requests = 5 - issued_books_count
        if requested_books_count >= remaining_requests:
            return make_response(jsonify({'error': f'You can only request {remaining_requests} more books since you have already issued {issued_books_count} books.'}), 400)

        new_request = Requested(
            user_id=user_id,
            bookid=bookid,
            status='Pending',
            requested_at=datetime.now()  
        )

        try:
            db.session.add(new_request)
            db.session.commit()
            response_message = {"message": "Book requested successfully", "request_id": new_request.request_id}
            if warning_message:
                response_message["warning"] = warning_message
            return make_response(jsonify(response_message), 201)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'error': 'An error occurred while requesting the book'}), 500)
    
    def options(self, *args, **kwargs):
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        return response
    
    
    
    
    
    
class ShowAllRequestsAPI(Resource):
    @token_required
    @roles_accepted('admin')
    @cache.cached(timeout=1)
    def get(self):
        try:
            search_query = request.args.get('search', '')
            query = Requested.query.join(User, Requested.user_id == User.id)\
                                   .join(eBooks, Requested.bookid == eBooks.book_id)\
                                   .join(eSection, eBooks.sectionid == eSection.section_id)\
                                   .add_columns(User.username, eBooks.book_name, eSection.section_name, Requested.requested_at, Requested.status, Requested.request_id)

            if search_query:
                query = query.filter(
                    or_(
                        User.username.ilike(f'%{search_query}%'),
                        eBooks.book_name.ilike(f'%{search_query}%'),
                        eSection.section_name.ilike(f'%{search_query}%')
                    )
                )

            requests = query.all()

            result = []
            for req in requests:
                result.append({
                    'username': req.username,
                    'book_name': req.book_name,
                    'section_name': req.section_name,
                    'requested_at': req.requested_at.isoformat(),
                    'status': req.status,
                    'request_id': req.request_id
                })

            return make_response(jsonify({'data': result}), 200)
        except Exception as e:
            print(e)
            return make_response(jsonify({'message': 'Failed to fetch requests'}), 500)
    
    def delete(self):
        try:
            data = request.get_json()
            request_id = data.get('request_id')

            requested_entry = db.session.get(Requested, request_id)
            if not requested_entry:
                return make_response(jsonify({'message': 'Request not found'}), 404)

            db.session.delete(requested_entry)
            db.session.commit()

            return make_response(jsonify({'message': 'Request deleted'}), 200)
        except Exception as e:
            print(e)
            db.session.rollback()
            return make_response(jsonify({'message': 'Failed to delete request'}), 500)


#======================================================================================================
#======================================================================================================
#==============================  API FOR ISSUED EBOOKS  ===============================================
#======================================================================================================
#======================================================================================================

class ShowAllIssuedBooksAPI(Resource):
    @token_required
    @roles_accepted('admin')
    def post(self):
        try:
            data = request.get_json()
            request_id = data.get('request_id')

            requested_entry = db.session.get(Requested, request_id)
            if not requested_entry:
                return make_response(jsonify({'message': 'Request not found'}), 404)

            issued_book = Issued.query.filter_by(bookid=requested_entry.bookid).first()
            if issued_book:
                issued_by_user = db.session.get(User, issued_book.user_id)
                return make_response(jsonify({'error': f'This book is already issued to {issued_by_user.username}. Cannot issue the same book to two different users.'}), 400)

            issued_at = datetime.now()
            return_before = issued_at + timedelta(days=1)  

            issued_entry = Issued(
                user_id=requested_entry.user_id,
                bookid=requested_entry.bookid,
                issued_at=issued_at,
                return_before=return_before,  
                status='Issued'
            )
            db.session.add(issued_entry)
            
            db.session.delete(requested_entry)
            db.session.commit()

            return make_response(jsonify({'message': 'Request approved, book issued, and request deleted'}), 200)
        except Exception as e:
            print(e)
            db.session.rollback()
            return make_response(jsonify({'message': 'Failed to approve request'}), 500)
    
    
    @token_required
    @roles_accepted('admin')
    @cache.cached(timeout=1)
    def get(self):
        try:
            search_query = request.args.get('search', '')
            query = db.session.query(
                Issued.issue_id,
                User.username,
                eBooks.book_name,
                eBooks.book_author,
                eSection.section_name,
                Issued.issued_at,
                Issued.return_before,  # Include return_before
                Issued.status
            ).join(User, Issued.user_id == User.id)\
             .join(eBooks, Issued.bookid == eBooks.book_id)\
             .join(eSection, eBooks.sectionid == eSection.section_id)

            if search_query:
                query = query.filter(
                    or_(
                        User.username.ilike(f'%{search_query}%'),
                        eBooks.book_name.ilike(f'%{search_query}%'),
                        eBooks.book_author.ilike(f'%{search_query}%'),
                        eSection.section_name.ilike(f'%{search_query}%')
                    )
                )

            issued_books = query.all()

            result = []
            for issued in issued_books:
                result.append({
                    'username': issued.username,
                    'book_name': issued.book_name,
                    'book_author': issued.book_author,
                    'section_name': issued.section_name,
                    'issued_at': issued.issued_at.isoformat() if issued.issued_at else None,
                    'return_before': issued.return_before.isoformat() if issued.return_before else None,
                    'status': issued.status,
                    'issue_id': issued.issue_id
                })

            return make_response(jsonify({'data': result}), 200)
        except Exception as e:
            print(e)
            return make_response(jsonify({'message': 'Failed to fetch issued books'}), 500)


    @token_required
    @roles_accepted('admin')
    def delete(self):
        try:
            data = request.get_json()
            issue_id = data.get('issue_id')

            issued_entry = Issued.query.get(issue_id)
            if not issued_entry:
                return make_response(jsonify({'message': 'Issued book not found'}), 404)

            db.session.delete(issued_entry)
            db.session.commit()

            return make_response(jsonify({'message': 'Issued book revoked and deleted'}), 200)
        except Exception as e:
            print(e)
            db.session.rollback()
            return make_response(jsonify({'message': 'Failed to revoke issued book'}), 500)
        
        
    def options(self, *args, **kwargs):
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        return response





class IssuedAPI(Resource):

    @token_required
    @roles_accepted('admin', 'user')
    @cache.cached(timeout=1)
    def get(self):
        user_id = request.args.get('user_id')
        if not user_id:
            return make_response(jsonify({'error': 'User ID is required'}), 400)

        try:
            issued_books = db.session.query(
                Issued,
                eBooks.book_id,
                eBooks.book_name,
                eBooks.DownloadPrice,  
                Issued.return_before,  
                eSection.section_name,
                User.username
            ).join(eBooks, Issued.bookid == eBooks.book_id)\
                .join(eSection, eBooks.sectionid == eSection.section_id)\
                .join(User, Issued.user_id == User.id)\
                .filter(Issued.user_id == user_id)\
                .all()

            data = [
                {
                    'username': req[6],  
                    'book_id': req[1],  
                    'book_name': req[2],  
                    'DownloadPrice': req[3],  
                    'section_name': req[5], 
                    'issued_at': req[0].issued_at.isoformat() if req[0].issued_at else 'N/A',  
                    'return_before': req[4].isoformat() if req[4] else 'N/A',  
                    'status': req[0].status,  
                    'issue_id': req[0].issue_id  
                }
                for req in issued_books
            ]

            return make_response(jsonify({"message": "get all issued books", "data": data}), 200)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)



    @token_required
    @roles_accepted('admin', 'user')
    def post(self):
        user_id = request.json.get('user_id')
        bookid = request.json.get('bookid')

        if not user_id or not bookid:
            return make_response(jsonify({'error': 'User ID and Book ID are required'}), 400)

        book = db.session.query(eBooks).filter_by(book_id=bookid).first()
        if not book:
            return make_response(jsonify({'error': 'Book not found'}), 404)

        existing_issue = Issued.query.filter_by(user_id=user_id, bookid=bookid).first()
        if existing_issue:
            return make_response(jsonify({'error': 'You have already issued this book'}), 400)

        new_issue = Issued(
            user_id=user_id,
            bookid=bookid,
            status='Issued',
            issued_at=datetime.now()
        )

        try:
            db.session.add(new_issue)
            db.session.commit()
            return make_response(jsonify({"message": "Book issued successfully", "issue_id": new_issue.issue_id}), 201)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'error': 'An error occurred while issuing the book'}), 500)


    @token_required
    @roles_accepted('admin', 'user')
    def delete(self):
        issue_id = request.json.get('issue_id')

        if not issue_id:
            return make_response(jsonify({'error': 'Issue ID is required'}), 400)

        issue = Issued.query.filter_by(issue_id=issue_id).first()
        if not issue:
            return make_response(jsonify({'error': 'Issue not found'}), 404)

        try:
            db.session.delete(issue)
            db.session.commit()
            return make_response(jsonify({"message": "Issue deleted successfully"}), 200)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'error': 'An error occurred while deleting the issue'}), 500)



#======================================================================================================
#======================================================================================================
#=========================  API FOR HANDLING PAYMENT AND FEEDBACK  ====================================
#======================================================================================================
#======================================================================================================


class PaymentAPI(Resource):
    
    def post(self):
        data = request.get_json()
        book_id = data.get('book_id')
        card_number = data.get('cardNumber')
        expiry_month = data.get('expiryMonth')
        expiry_year = data.get('expiryYear')
        cv_code = data.get('cvCode')
        download_price = data.get('downloadPrice')  

        book = db.session.get(eBooks, book_id)

        if not book:
            return make_response(jsonify({'message': 'Book not found'}), 404)

        if book.DownloadPrice == float(download_price):  
            return make_response(jsonify({'message': 'Payment successful'}), 200)
        else:
            return make_response(jsonify({'message': 'Invalid price'}), 400)
        


class FeedbackAPI(Resource):
    
    def post(self):
        data = request.get_json()

        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        rating = data.get('rating')
        message = data.get('message')
        user_id = data.get('user_id')  
        book_id = data.get('book_id')  

        if not all([name, email, phone, rating, message, user_id, book_id]):
            return jsonify({"error": "All fields are required."}), 400

        feedback = Feedback(
            name=name,
            email=email,
            feedback_message=message,
            rating_value=rating,
            feedback_user_id=user_id,
            book_id=book_id
        )

        db.session.add(feedback)
        db.session.commit()

        return make_response(jsonify({"message": "Feedback submitted successfully!"}), 201)



#======================================================================================================
#======================================================================================================
#==============================  ADDING RESOURCES TO API ENDPOINTS  ===================================
#======================================================================================================
#======================================================================================================


api.add_resource(FeedbackAPI, '/api/feedback')

api.add_resource(PaymentAPI, '/api/payment')
api.add_resource(IssuedAPI, '/api/issued_books')

api.add_resource(ShowAllRequestsAPI, '/api/showallrequests')
api.add_resource(ShowAllIssuedBooksAPI, '/api/approve_request')
    
api.add_resource(Librarian_Login, '/api/Librarian_login')
api.add_resource(User_Login, '/api/User_login')
api.add_resource(register, '/api/register')

api.add_resource(EbooksResource, '/api/ebooks')
api.add_resource(EbooksSpecific, '/api/ebooks/<int:book_id>')

api.add_resource(Ebooks_Read_PDF_API, '/api/ebooks/<int:book_id>/pdf')
api.add_resource(Ebooks_Download_PDF_API, '/api/ebooksDownload/<int:book_id>/pdf')

api.add_resource(EsectionResource, '/api/esection')
api.add_resource(EsectionSpecific, '/api/esection/<int:section_id>')

api.add_resource(RequestAPI, '/api/request_book')





security = Security(app, user_datastore, api)



def generate_auth_token(user):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = s.dumps({'id': user.id})
    return token





        
with app.app_context():
    
    #db.drop_all()
    
    db.create_all()
    

    user_datastore.find_or_create_role(name = 'admin', description = 'Librarian')
    user_datastore.find_or_create_role(name = 'user', description = 'User')
    db.session.commit()


    if not user_datastore.find_user(email = 'Librarian@Pustakalay.com'):
        admin_user = user_datastore.create_user(
            email='Librarian@Pustakalay.com',
            password=hash_password('admin'),
            username='Librarian',
            authentication_token = '',
            roles=['admin', 'user']
        )
        admin_token = generate_auth_token(admin_user)
        admin_user.authentication_token = admin_token
        db.session.commit()
        
    if not User.query.filter_by(username = 'Rishi').first():
        test_user = user_datastore.create_user(
            username='Rishi',
            password=hash_password('rishi'),
            email='Rishi@Pustakalay.com',
            authentication_token = '',
            roles=['user']
        )
        user_token = generate_auth_token(test_user)
        test_user.authentication_token = user_token
        user_datastore.add_role_to_user(test_user, 'user')
        db.session.commit()
        
    


if __name__ == '__main__':
    app.run(debug = True, port=5000)
    
    
    