
from database import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    balance = db.Column(db.Float, default=0.0)
    avatar_initials = db.Column(db.String(4), default='??')
    phone = db.Column(db.String(20), nullable=True)
    bio = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_verified = db.Column(db.Boolean, default=True)

    sent_transactions = db.relationship('Transaction', foreign_keys='Transaction.sender_id', backref='sender', lazy='dynamic')
    received_transactions = db.relationship('Transaction', foreign_keys='Transaction.receiver_id', backref='receiver', lazy='dynamic')
    contacts = db.relationship('Contact', foreign_keys='Contact.user_id', backref='user', lazy='dynamic')

    def get_recent_transactions(self, limit=10):
        from models.transaction import Transaction
        from sqlalchemy import or_
        return Transaction.query.filter(
            or_(Transaction.sender_id == self.id, Transaction.receiver_id == self.id)
        ).order_by(Transaction.created_at.desc()).limit(limit).all()

    def get_all_transactions(self):
        from models.transaction import Transaction
        from sqlalchemy import or_
        return Transaction.query.filter(
            or_(Transaction.sender_id == self.id, Transaction.receiver_id == self.id)
        ).order_by(Transaction.created_at.desc()).all()
