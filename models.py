from extensions import db
from flask_login import UserMixin
from datetime import datetime
import re
from decimal import Decimal

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(2000))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(15), unique=True, nullable=True)
    preferred_currency = db.Column(db.String(3), default='INR')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    # Relationships
    account = db.relationship('UserAccount', backref='user', uselist=False, cascade="all, delete-orphan")
    sent_transactions = db.relationship('Transaction', foreign_keys='Transaction.sender_id', backref='sender', cascade="all, delete-orphan")
    received_transactions = db.relationship('Transaction', foreign_keys='Transaction.receiver_id', backref='receiver', cascade="all, delete-orphan")

    def __init__(self, **kwargs):
        # Set default currency if not provided
        if 'preferred_currency' not in kwargs:
            kwargs['preferred_currency'] = 'INR'
            
        super(User, self).__init__(**kwargs)
        
        # Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            raise ValueError("Invalid email format")
        # Validate username (alphanumeric, underscore, and dot only)
        if not re.match(r"^[A-Za-z][A-Za-z0-9_.]*$", self.username):
            raise ValueError("Username must start with a letter and can only contain letters, numbers, dots or underscores")
        # Validate phone number if provided
        if self.phone and not re.match(r'^\+?[0-9]{10,15}$', self.phone):
            raise ValueError("Invalid phone number format")
        # Validate currency code
        if self.preferred_currency not in ['USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'INR', 'CNY']:
            raise ValueError("Invalid currency code")

class UserAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    balance = db.Column(db.Numeric(10, 2), default=Decimal('0.00'))
    currency = db.Column(db.String(3), default='INR', nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        # Set default currency if not provided
        if 'currency' not in kwargs:
            kwargs['currency'] = 'INR'
        if 'balance' in kwargs:
            kwargs['balance'] = Decimal(str(kwargs['balance']))
            
        super(UserAccount, self).__init__(**kwargs)
        
        # Validate currency code
        if self.currency not in ['USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'INR', 'CNY']:
            raise ValueError("Invalid currency code")
        # Validate balance
        if self.balance < Decimal('0.00'):
            raise ValueError("Balance cannot be negative")

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(3), default='INR', nullable=False)
    description = db.Column(db.String(200), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='completed')  # completed, pending, failed
    transaction_type = db.Column(db.String(20), nullable=False)  # deposit, transfer, withdrawal

    def __init__(self, **kwargs):
        super(Transaction, self).__init__(**kwargs)
        # Validate amount
        if 'amount' in kwargs:
            self.amount = Decimal(str(kwargs['amount']))
        if self.amount <= Decimal('0.00'):
            raise ValueError("Transaction amount must be greater than 0")
        # Validate status
        if self.status not in ['completed', 'pending', 'failed']:
            raise ValueError("Invalid transaction status")
        # Validate transaction type
        if self.transaction_type not in ['deposit', 'transfer', 'withdrawal']:
            raise ValueError("Invalid transaction type")
        # Validate sender and receiver are different for transfers
        if self.transaction_type == 'transfer' and self.sender_id == self.receiver_id:
            raise ValueError("Sender and receiver cannot be the same for transfers")
        # Validate currency
        if self.currency not in ['USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'INR', 'CNY']:
            raise ValueError("Invalid currency code")