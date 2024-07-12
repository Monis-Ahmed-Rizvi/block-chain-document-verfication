from app import db
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
import secrets

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    email_verified = db.Column(db.Boolean, default=False)
    email_verification_token = db.Column(db.String(32))
    email_verification_sent_at = db.Column(db.DateTime)
    documents = db.relationship('Document', backref='owner', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_email_verification_token(self):
        self.email_verification_token = secrets.token_hex(16)
        self.email_verification_sent_at = datetime.utcnow()
        db.session.commit()

    def verify_email(self, token):
        if self.email_verification_token == token and \
           datetime.utcnow() - self.email_verification_sent_at < timedelta(hours=24):
            self.email_verified = True
            self.email_verification_token = None
            self.email_verification_sent_at = None
            db.session.commit()
            return True
        return False

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(256))
    file_hash = db.Column(db.String(64), index=True, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    blockchain_tx_hash = db.Column(db.String(66))  # For future blockchain integration

    @staticmethod
    def generate_hash(file_content):
        return hashlib.sha256(file_content).hexdigest()