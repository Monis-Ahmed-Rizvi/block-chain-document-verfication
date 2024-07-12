from flask import jsonify, request, Blueprint, current_app, url_for
from app import db, mail, limiter
from app.models import User, Document
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.utils import secure_filename
from flask_mail import Message
from app.errors import bad_request
import os

bp = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/', methods=['GET'])
def root():
    return jsonify({"message": "Welcome to the Document Verification API"}), 200

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Missing required fields"}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already exists"}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already exists"}), 400
    
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    user.generate_email_verification_token()
    
    db.session.add(user)
    db.session.commit()
    
    send_verification_email(user)
    
    return jsonify({"message": "User registered successfully. Please check your email to verify your account."}), 201

@bp.route('/verify-email/<token>', methods=['GET'])
def verify_email(token):
    user = User.query.filter_by(email_verification_token=token).first()
    if user and user.verify_email(token):
        return jsonify({"message": "Email verified successfully"}), 200
    return jsonify({"error": "Invalid or expired token"}), 400

@bp.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return bad_request('Missing username or password')
    
    user = User.query.filter_by(username=data['username']).first()
    
    if user and user.check_password(data['password']):
        if not user.email_verified:
            return bad_request('Please verify your email before logging in')
        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token}), 200
    
    return bad_request('Invalid username or password')

@bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_document():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_content = file.read()
        file_hash = Document.generate_hash(file_content)
        
        existing_doc = Document.query.filter_by(file_hash=file_hash).first()
        if existing_doc:
            return jsonify({"error": "File already exists", "document_id": existing_doc.id}), 409
        
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        with open(file_path, 'wb') as f:
            f.write(file_content)
        
        new_document = Document(filename=filename, file_hash=file_hash, user_id=get_jwt_identity())
        db.session.add(new_document)
        db.session.commit()
        
        return jsonify({
            "message": "File successfully uploaded",
            "filename": filename,
            "document_id": new_document.id
        }), 201
    return jsonify({"error": "File type not allowed"}), 400

@bp.route('/documents', methods=['GET'])
@jwt_required()
def get_user_documents():
    user_id = get_jwt_identity()
    documents = Document.query.filter_by(user_id=user_id).all()
    return jsonify({
        "documents": [
            {
                "id": doc.id,
                "filename": doc.filename,
                "timestamp": doc.timestamp.isoformat(),
                "file_hash": doc.file_hash
            } for doc in documents
        ]
    }), 200

@bp.route('/verify/<int:document_id>', methods=['GET'])
@jwt_required()
def verify_document(document_id):
    document = Document.query.get_or_404(document_id)
    if document.user_id != get_jwt_identity():
        return jsonify({"error": "Unauthorized"}), 403
    
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], document.filename)
    with open(file_path, 'rb') as f:
        file_content = f.read()
    
    calculated_hash = Document.generate_hash(file_content)
    is_valid = calculated_hash == document.file_hash
    
    return jsonify({
        "document_id": document.id,
        "filename": document.filename,
        "is_valid": is_valid,
        "stored_hash": document.file_hash,
        "calculated_hash": calculated_hash
    }), 200

def send_verification_email(user):
    token = user.email_verification_token
    msg = Message('Verify Your Email',
                  sender='noreply@yourdomain.com',
                  recipients=[user.email])
    msg.body = f'''To verify your email, visit the following link:
{url_for('main.verify_email', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)