import os
from datetime import datetime, timedelta
from io import BytesIO

from flask import current_app, jsonify, make_response, request, send_file, send_from_directory
from flask_restful import Resource
from flask_security import current_user, login_user, roles_accepted
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError

from auth_utils import check_password, hash_password, token_required
from config import cache
from models import (
    Feedback,
    Issued,
    Requested,
    User,
    db,
    eBooks,
    eSection,
    user_datastore,
)


class User_Login(Resource):
    def post(self):
        data = request.get_json()
        email = data['email']
        password = data['password']
        user = user_datastore.find_user(email=email)
        if user:
            if check_password(user.password, password):
                login_user(user)
                token = user.get_auth_token()
                db.session.commit()
                role = 'admin' if current_user.has_role('admin') else 'user'
                return make_response(
                    jsonify(
                        {
                            'token': token,
                            'email': user.email,
                            'id': user.id,
                            'role': role,
                            'username': user.username,
                            'message': 'Login Successful',
                        }
                    ),
                    200,
                )
            return make_response(
                jsonify({'message': 'Wrong Password', 'password': check_password(user.password, password)}),
                401,
            )
        return make_response(jsonify({'message': 'Incorrect Email', 'email': email}), 404)

    def options(self, *args, **kwargs):
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        return response


class Librarian_Login(Resource):
    def post(self):
        data = request.get_json()
        email = data['email']
        password = data['password']
        user = user_datastore.find_user(email=email)

        if user:
            if check_password(user.password, password):
                login_user(user)
                token = user.get_auth_token()
                db.session.commit()

                role = 'admin' if current_user.has_role('admin') else 'user'
                return make_response(
                    jsonify(
                        {
                            'token': token,
                            'email': user.email,
                            'id': user.id,
                            'role': role,
                            'username': user.username,
                            'message': 'Login Successful',
                        }
                    ),
                    200,
                )
            return make_response(
                jsonify({'message': 'Wrong Password', 'password': check_password(user.password, password)}),
                401,
            )
        return make_response(jsonify({'message': 'Incorrect Email', 'email': email}), 404)

    def options(self, *args, **kwargs):
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        return response


class register(Resource):
    def post(self):
        data = request.get_json()
        email = data['email']
        password = data['password']
        username = data['username']
        if not email:
            return make_response(jsonify({'message': 'Email required'}), 400)
        if not password:
            return make_response(jsonify({'message': 'Password required'}), 400)
        if not username:
            return make_response(jsonify({'message': 'Username required'}), 400)

        user_check_email = user_datastore.find_user(email=email)
        user_check_username = user_datastore.find_user(username=username)
        if user_check_email:
            return make_response(jsonify({'message': 'User Email already present'}), 400)
        if user_check_username:
            return make_response(jsonify({'message': 'Username already present'}), 400)

        hashed_password = hash_password(password)

        user = user_datastore.create_user(email=email, password=hashed_password, username=username)

        user_datastore.add_role_to_user(user, 'user')
        db.session.commit()
        return make_response(
            jsonify({'message': 'User registered successfully', 'username': user.username, 'email': user.email}),
            201,
        )

    def options(self, *args, **kwargs):
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        return response


class EsectionResource(Resource):
    @token_required
    @roles_accepted('admin', 'user')
    @cache.cached(timeout=1)
    def get(self):
        search_query = request.args.get('search', '')

        query = db.session.query(eSection)
        if search_query:
            query = query.filter(
                or_(
                    eSection.section_name.ilike(f'%{search_query}%'),
                    eSection.description.ilike(f'%{search_query}%'),
                )
            )

        sections = query.all()
        data = []
        for section in sections:
            data.append(
                {
                    'section_id': section.section_id,
                    'section_name': section.section_name,
                    'date_created': section.date_created.isoformat(),
                    'description': section.description,
                    'created_by': section.created_by,
                    'updated_by': section.updated_by,
                    'updated_at': section.updated_at.isoformat() if section.updated_at else None,
                }
            )

        if not data:
            return make_response(jsonify({'message': 'No Sections Found'}), 404)
        return make_response(jsonify({'message': 'Get All Sections', 'data': data}), 200)

    @token_required
    @roles_accepted('admin')
    def post(self):
        data = request.get_json()
        section_name = data['section_name']
        if not section_name:
            return make_response(jsonify({'message': 'Name required'}), 400)
        description = data['description']
        if not description:
            return make_response(jsonify({'message': 'Description required'}), 400)

        section = eSection(
            section_name=section_name,
            description=description,
            status=True if current_user.has_role('admin') else False,
            date_created=datetime.now(),
            created_by=current_user.id,
        )
        db.session.add(section)
        db.session.commit()
        return make_response(
            jsonify(
                {
                    'message': 'E-Book_Section Created Successfully',
                    'section_id': section.section_id,
                    'section_name': section.section_name,
                    'status': section.status,
                }
            ),
            201,
        )

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
        section = eSection.query.filter_by(section_id=section_id).first()
        if not section:
            return make_response(jsonify({'message': 'Section with this id not found'}), 404)
        payload = {
            'section_id': section.section_id,
            'section_name': section.section_name,
            'date_created': section.date_created.isoformat(),
            'description': section.description,
            'created_by': section.created_by,
            'updated_by': section.updated_by,
            'updated_at': section.updated_at.isoformat() if section.updated_at else None,
        }
        return make_response(jsonify({'message': 'Found Section with this id', 'data': payload}), 200)

    @token_required
    @roles_accepted('admin')
    def put(self, section_id):
        try:
            section = eSection.query.filter_by(section_id=section_id).first()
            if not section:
                return make_response(jsonify({'message': 'Section with this id not found'}), 404)
            data = request.get_json()
            section_name = data['section_name']
            if not section_name:
                return make_response(jsonify({'message': 'Name required'}), 400)
            description = data['description']
            if not description:
                return make_response(jsonify({'message': 'Description required'}), 400)

            section.section_name = section_name
            section.description = description
            section.updated_at = datetime.now()
            section.updated_by = current_user.id
            section.status = True if current_user.has_role('admin') else False
            db.session.commit()
            return make_response(jsonify({'message': 'Updated', 'section_id': section_id}), 200)

        except SQLAlchemyError as exc:
            db.session.rollback()
            return jsonify({'message': 'Error updating section', 'error': str(exc)}), 500
        except Exception as exc:
            db.session.rollback()
            return jsonify({'message': 'Unexpected error', 'error': str(exc)}), 500

    @token_required
    @roles_accepted('admin')
    def delete(self, section_id):
        section = eSection.query.filter_by(section_id=section_id).first()
        if not section:
            return make_response(jsonify({'message': 'No eSection found by that id'}), 404)

        books_in_section = eBooks.query.filter_by(sectionid=section_id).all()
        if books_in_section:
            return make_response(jsonify({'message': 'Cannot delete eSection as it contains eBooks'}), 400)

        db.session.delete(section)
        db.session.commit()
        return jsonify({'message': 'Deleted Specific eSection', 'section_id': section_id})

    def options(self, *args, **kwargs):
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        return response


class EbooksResource(Resource):
    @token_required
    @roles_accepted('admin')
    def post(self):
        book_name = request.form.get('book_name')
        if not book_name:
            return make_response(jsonify({'message': 'Book name is required'}), 400)

        book_author = request.form.get('book_author')
        if not book_author:
            return make_response(jsonify({'message': 'Book Author is required'}), 400)

        download_price = request.form.get('DownloadPrice')
        if not download_price:
            return make_response(jsonify({'message': 'Please Decide Download Price'}), 400)

        sectionid = request.form.get('section_id')
        if not sectionid:
            return make_response(jsonify({'message': 'Section ID not found'}), 400)

        if 'book_content' not in request.files:
            return make_response(jsonify({'message': 'No file part'}), 400)

        book_content = request.files['book_content']
        if book_content.filename == '':
            return make_response(jsonify({'message': 'No selected file'}), 400)

        ebook = eBooks(
            book_name=book_name,
            book_author=book_author,
            DownloadPrice=download_price,
            sectionid=sectionid,
            book_content=book_content.read(),
            created_by=current_user.id,
            date_created=datetime.now(),
        )
        db.session.add(ebook)
        db.session.commit()

        filename = f'{ebook.book_id}.pdf'
        pdf_path = os.path.join(current_app.instance_path, filename)

        book_content.seek(0)
        book_content.save(pdf_path)

        return make_response(
            jsonify({'message': 'eBook Created Successfully', 'book_id': ebook.book_id, 'book_name': ebook.book_name}),
            201,
        )

    @token_required
    @roles_accepted('admin', 'user')
    @cache.cached(timeout=1)
    def get(self):
        search_query = request.args.get('search', '')
        query = db.session.query(eBooks)
        if search_query:
            query = query.filter(
                or_(eBooks.book_name.ilike(f'%{search_query}%'), eBooks.book_author.ilike(f'%{search_query}%'))
            )

        ebooks = query.all()
        data = []
        for ebook in ebooks:
            data.append(
                {
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
            )

        if not data:
            return make_response(jsonify({'message': 'No eBook Found'}), 404)
        return make_response(jsonify({'message': 'Get all eBooks', 'EBdata': data}), 200)

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
            return make_response(jsonify({'message': 'No eBook found by that id'}), 404)

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
        return jsonify({'message': 'Get specific eBook', 'data': data})

    @token_required
    @roles_accepted('admin')
    def put(self, book_id):
        ebook = eBooks.query.filter_by(book_id=book_id).first()
        if not ebook:
            return make_response(jsonify({'message': 'No eBook found by that id'}), 404)

        book_name = request.form.get('book_name')
        book_author = request.form.get('book_author')
        download_price = request.form.get('DownloadPrice')

        if not book_name:
            return make_response(jsonify({'message': 'Book name is required'}), 400)
        if not book_author:
            return make_response(jsonify({'message': 'Book author is required'}), 400)
        if not download_price:
            return make_response(jsonify({'message': 'Download price must be specified'}), 400)

        if 'book_content' in request.files:
            book_content = request.files['book_content']
            if book_content.filename == '':
                return make_response(jsonify({'message': 'No file selected'}), 400)

            file_content = book_content.read()
            if not file_content:
                return make_response(jsonify({'message': 'File content is empty'}), 400)

            filename = f'{book_id}.pdf'
            pdf_path = os.path.join(current_app.instance_path, filename)

            book_content.seek(0)
            book_content.save(pdf_path)

            ebook.book_content = file_content

        ebook.book_name = book_name
        ebook.book_author = book_author
        ebook.DownloadPrice = download_price
        ebook.updated_at = datetime.now()
        ebook.updated_by = current_user.id

        try:
            db.session.commit()
            return make_response(jsonify({'message': 'Book updated successfully', 'book_id': book_id}), 200)
        except Exception as exc:
            db.session.rollback()
            return make_response(jsonify({'message': 'Failed to update the book', 'error': str(exc)}), 500)

    @token_required
    @roles_accepted('admin')
    def delete(self, book_id):
        ebook = eBooks.query.filter_by(book_id=book_id).first()
        if not ebook:
            return make_response(jsonify({'message': 'No eBook found by that id'}), 404)

        issued_entry = Issued.query.filter_by(bookid=book_id).first()
        if issued_entry:
            user = User.query.filter_by(id=issued_entry.user_id).first()
            return make_response(
                jsonify({'message': f'This eBook is currently issued by {user.username} and cannot be deleted'}), 400
            )

        db.session.delete(ebook)
        db.session.commit()
        return jsonify({'message': 'Deleted specific eBook', 'book_id': book_id})

    def options(self, *args, **kwargs):
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        return response


class Ebooks_Download_PDF_API(Resource):
    def get(self, book_id):
        ebook = eBooks.query.filter_by(book_id=book_id).first()
        if not ebook:
            return jsonify({'message': 'No eBook found by that id'}), 404

        if not ebook.book_content:
            return jsonify({'message': 'No content available for this book'}), 404

        file_stream = BytesIO(ebook.book_content)
        return make_response(
            send_file(
                file_stream,
                mimetype='application/pdf',
                as_attachment=True,
                download_name=f'{ebook.book_name}.pdf',
            )
        )


class Ebooks_Read_PDF_API(Resource):
    def get(self, book_id):
        ebook = eBooks.query.filter_by(book_id=book_id).first()
        if not ebook:
            return jsonify({'message': 'No eBook found by that id'}), 404

        if not ebook.book_content:
            return jsonify({'message': 'No content available for this book'}), 404

        file_stream = BytesIO(ebook.book_content)
        return make_response(send_file(file_stream, mimetype='application/pdf', as_attachment=False))


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
            query = (
                db.session.query(Requested, eBooks.book_name, eBooks.book_author, eSection.section_name, User.username)
                .join(eBooks, Requested.bookid == eBooks.book_id)
                .join(eSection, eBooks.sectionid == eSection.section_id)
                .join(User, Requested.user_id == User.id)
                .filter(Requested.user_id == user_id)
            )

            if search_query:
                query = query.filter(
                    or_(
                        eBooks.book_name.ilike(f'%{search_query}%'),
                        eBooks.book_author.ilike(f'%{search_query}%'),
                        eSection.section_name.ilike(f'%{search_query}%'),
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
                    'status': req[0].status,
                }
                for req in requested_books
            ]

            return make_response(jsonify({'message': 'get all requests', 'data': data}), 200)

        except Exception:
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
            warning_message = (
                f'This book is already requested by {requested_by_user.username}, '
                'chances of your request getting approved are less, since requests are approved '
                'on a first come first serve basis.'
            )

        issued_books_count = db.session.query(Issued).filter_by(user_id=user_id).count()
        requested_books_count = db.session.query(Requested).filter_by(user_id=user_id).count()
        total_books = issued_books_count + requested_books_count

        if total_books >= 5:
            return make_response(
                jsonify(
                    {
                        'error': (
                            'You cannot request more than 5 books. '
                            'Please return some books to make new requests.'
                        )
                    }
                ),
                400,
            )

        remaining_requests = 5 - issued_books_count
        if requested_books_count >= remaining_requests:
            return make_response(
                jsonify(
                    {
                        'error': (
                            f'You can only request {remaining_requests} more books since '
                            f'you have already issued {issued_books_count} books.'
                        )
                    }
                ),
                400,
            )

        new_request = Requested(user_id=user_id, bookid=bookid, status='Pending', requested_at=datetime.now())

        try:
            db.session.add(new_request)
            db.session.commit()
            response_message = {'message': 'Book requested successfully', 'request_id': new_request.request_id}
            if warning_message:
                response_message['warning'] = warning_message
            return make_response(jsonify(response_message), 201)
        except Exception:
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
            query = (
                Requested.query.join(User, Requested.user_id == User.id)
                .join(eBooks, Requested.bookid == eBooks.book_id)
                .join(eSection, eBooks.sectionid == eSection.section_id)
                .add_columns(
                    User.username,
                    eBooks.book_name,
                    eSection.section_name,
                    Requested.requested_at,
                    Requested.status,
                    Requested.request_id,
                )
            )

            if search_query:
                query = query.filter(
                    or_(
                        User.username.ilike(f'%{search_query}%'),
                        eBooks.book_name.ilike(f'%{search_query}%'),
                        eSection.section_name.ilike(f'%{search_query}%'),
                    )
                )

            requests = query.all()

            result = []
            for req in requests:
                result.append(
                    {
                        'username': req.username,
                        'book_name': req.book_name,
                        'section_name': req.section_name,
                        'requested_at': req.requested_at.isoformat(),
                        'status': req.status,
                        'request_id': req.request_id,
                    }
                )

            return make_response(jsonify({'data': result}), 200)
        except Exception:
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
        except Exception:
            db.session.rollback()
            return make_response(jsonify({'message': 'Failed to delete request'}), 500)


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
                return make_response(
                    jsonify(
                        {
                            'error': (
                                f'This book is already issued to {issued_by_user.username}. '
                                'Cannot issue the same book to two different users.'
                            )
                        }
                    ),
                    400,
                )

            issued_at = datetime.now()
            return_before = issued_at + timedelta(days=1)

            issued_entry = Issued(
                user_id=requested_entry.user_id,
                bookid=requested_entry.bookid,
                issued_at=issued_at,
                return_before=return_before,
                status='Issued',
            )
            db.session.add(issued_entry)

            db.session.delete(requested_entry)
            db.session.commit()

            return make_response(jsonify({'message': 'Request approved, book issued, and request deleted'}), 200)
        except Exception:
            db.session.rollback()
            return make_response(jsonify({'message': 'Failed to approve request'}), 500)

    @token_required
    @roles_accepted('admin')
    @cache.cached(timeout=1)
    def get(self):
        try:
            search_query = request.args.get('search', '')
            query = (
                db.session.query(
                    Issued.issue_id,
                    User.username,
                    eBooks.book_name,
                    eBooks.book_author,
                    eSection.section_name,
                    Issued.issued_at,
                    Issued.return_before,
                    Issued.status,
                )
                .join(User, Issued.user_id == User.id)
                .join(eBooks, Issued.bookid == eBooks.book_id)
                .join(eSection, eBooks.sectionid == eSection.section_id)
            )

            if search_query:
                query = query.filter(
                    or_(
                        User.username.ilike(f'%{search_query}%'),
                        eBooks.book_name.ilike(f'%{search_query}%'),
                        eBooks.book_author.ilike(f'%{search_query}%'),
                        eSection.section_name.ilike(f'%{search_query}%'),
                    )
                )

            issued_books = query.all()

            result = []
            for issued in issued_books:
                result.append(
                    {
                        'username': issued.username,
                        'book_name': issued.book_name,
                        'book_author': issued.book_author,
                        'section_name': issued.section_name,
                        'issued_at': issued.issued_at.isoformat() if issued.issued_at else None,
                        'return_before': issued.return_before.isoformat() if issued.return_before else None,
                        'status': issued.status,
                        'issue_id': issued.issue_id,
                    }
                )

            return make_response(jsonify({'data': result}), 200)
        except Exception:
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
        except Exception:
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
            issued_books = (
                db.session.query(
                    Issued,
                    eBooks.book_id,
                    eBooks.book_name,
                    eBooks.DownloadPrice,
                    Issued.return_before,
                    eSection.section_name,
                    User.username,
                )
                .join(eBooks, Issued.bookid == eBooks.book_id)
                .join(eSection, eBooks.sectionid == eSection.section_id)
                .join(User, Issued.user_id == User.id)
                .filter(Issued.user_id == user_id)
                .all()
            )

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
                    'issue_id': req[0].issue_id,
                }
                for req in issued_books
            ]

            return make_response(jsonify({'message': 'get all issued books', 'data': data}), 200)
        except Exception as exc:
            return make_response(jsonify({'error': str(exc)}), 500)

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

        new_issue = Issued(user_id=user_id, bookid=bookid, status='Issued', issued_at=datetime.now())

        try:
            db.session.add(new_issue)
            db.session.commit()
            return make_response(jsonify({'message': 'Book issued successfully', 'issue_id': new_issue.issue_id}), 201)
        except Exception:
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
            return make_response(jsonify({'message': 'Issue deleted successfully'}), 200)
        except Exception:
            db.session.rollback()
            return make_response(jsonify({'error': 'An error occurred while deleting the issue'}), 500)


class PaymentAPI(Resource):
    def post(self):
        data = request.get_json()
        book_id = data.get('book_id')
        download_price = data.get('downloadPrice')

        book = db.session.get(eBooks, book_id)

        if not book:
            return make_response(jsonify({'message': 'Book not found'}), 404)

        if book.DownloadPrice == float(download_price):
            return make_response(jsonify({'message': 'Payment successful'}), 200)
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
            return jsonify({'error': 'All fields are required.'}), 400

        feedback = Feedback(
            name=name,
            email=email,
            feedback_message=message,
            rating_value=rating,
            feedback_user_id=user_id,
            book_id=book_id,
        )

        db.session.add(feedback)
        db.session.commit()

        return make_response(jsonify({'message': 'Feedback submitted successfully!'}), 201)


def serve_pdf(filename):
    return send_from_directory(os.path.join(current_app.instance_path), filename)


def register_resources(api):
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
