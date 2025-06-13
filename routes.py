from flask import render_template, redirect, url_for, flash, request, session, current_app
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from models import User, Transaction, UserAccount
from forms import LoginForm, RegistrationForm, SendMoneyForm, AddMoneyForm, ProfileUpdateForm, CurrencyConversionForm
import logging
from datetime import datetime
from currency_service import convert_amount, format_currency, get_currency_symbol
from decimal import Decimal

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def register_routes(app):
    @app.route('/')
    def index():
        """Landing page route"""
        return render_template('index.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """User registration route"""
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))

        form = RegistrationForm()

        if form.validate_on_submit():
            try:
                # Clear old session data if any
                session.clear()

                logger.info(f"Attempting to register user: {form.username.data}")

                # Check if username or email already exists
                existing_user = User.query.filter(
                    (User.username == form.username.data) | 
                    (User.email == form.email.data)
                ).first()

                if existing_user:
                    if existing_user.username == form.username.data:
                        logger.warning(f"Username already exists: {form.username.data}")
                        flash('Username already exists. Please choose a different one.', 'danger')
                    else:
                        logger.warning(f"Email already registered: {form.email.data}")
                        flash('Email already registered. Please use a different email.', 'danger')
                    return render_template('register.html', form=form)

                # Validate phone number if provided
                if form.phone.data:
                    phone_user = User.query.filter_by(phone=form.phone.data).first()
                    if phone_user:
                        logger.warning(f"Phone number already registered: {form.phone.data}")
                        flash('Phone number already registered. Please use a different number.', 'danger')
                        return render_template('register.html', form=form)

                # Create new user with default currency
                hashed_password = generate_password_hash(form.password.data)
                new_user = User(
                    username=form.username.data,
                    email=form.email.data,
                    password_hash=hashed_password,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    phone=form.phone.data,
                    preferred_currency='INR'  # Set default currency to INR
                )

                db.session.add(new_user)
                db.session.flush()  # Flush to get the user ID
                logger.info(f"Created new user with ID: {new_user.id}")

                # Create account for the user with initial balance of 0
                user_account = UserAccount(
                    user_id=new_user.id,
                    balance=0.0,
                    currency='INR'  # Set account currency to INR
                )
                db.session.add(user_account)

                db.session.commit()
                logger.info(f"Successfully created account for user: {new_user.username}")

                flash('Registration successful! You can now log in.', 'success')
                return redirect(url_for('login'))

            except Exception as e:
                db.session.rollback()
                logger.error(f"Error in registration: {str(e)}")
                logger.error(f"Form data: {form.data}")
                logger.exception("Exception details:")  # Log full stack trace
                flash(f'Registration error: {str(e)}', 'danger')
                return render_template('register.html', form=form)

        # Log form validation errors
        if form.errors:
            logger.error(f"Form validation errors: {form.errors}")
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"{field}: {error}", 'danger')

        return render_template('register.html', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """User login route"""
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
            
        form = LoginForm()
        
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            
            if user and check_password_hash(user.password_hash, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                flash('Login successful!', 'success')
                logger.info(f"User logged in: {user.username}")
                return redirect(next_page or url_for('dashboard'))
            else:
                flash('Invalid username or password', 'danger')
                logger.warning(f"Failed login attempt for username: {form.username.data}")
                
        return render_template('login.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        """User logout route"""
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('index'))

    @app.route('/dashboard')
    @login_required
    def dashboard():
        """User dashboard route"""
        # Get user account info
        account = current_user.account
        
        # Get recent transactions (sent and received)
        sent_transactions = Transaction.query.filter_by(sender_id=current_user.id).order_by(Transaction.timestamp.desc()).limit(5).all()
        received_transactions = Transaction.query.filter_by(receiver_id=current_user.id).order_by(Transaction.timestamp.desc()).limit(5).all()
        
        # Get all transactions for the recent activity table
        all_transactions = Transaction.query.filter(
            (Transaction.sender_id == current_user.id) | 
            (Transaction.receiver_id == current_user.id)
        ).order_by(Transaction.timestamp.desc()).limit(10).all()
        
        # Get current display currency (from session or user preference)
        display_currency = session.get('display_currency', current_user.preferred_currency or 'INR')
        account_currency = account.currency if account else 'INR'
        
        # Create currency conversion form
        currency_form = CurrencyConversionForm()
        currency_form.currency.default = display_currency
        currency_form.process()
        
        # Calculate income and expenses in the account's currency
        income = sum(tx.amount for tx in Transaction.query.filter_by(receiver_id=current_user.id).all())
        expenses = sum(tx.amount for tx in Transaction.query.filter(
            (Transaction.sender_id == current_user.id) & 
            (Transaction.transaction_type != 'deposit')
        ).all())
        
        # Format monetary values in the user's preferred currency
        formatted_balance = format_currency(
            convert_amount(account.balance, account_currency, display_currency) if account else 0, 
            display_currency
        )
        
        formatted_income = format_currency(
            convert_amount(income, account_currency, display_currency), 
            display_currency
        )
        
        formatted_expenses = format_currency(
            convert_amount(expenses, account_currency, display_currency), 
            display_currency
        )
        
        # Convert transaction amounts for display
        for tx in all_transactions:
            tx.formatted_amount = format_currency(
                convert_amount(tx.amount, tx.currency, display_currency),
                display_currency
            )
        
        return render_template(
            'dashboard.html',
            user=current_user,
            account=account,
            sent_transactions=sent_transactions,
            received_transactions=received_transactions,
            all_transactions=all_transactions,
            income=income,
            expenses=expenses,
            formatted_balance=formatted_balance,
            formatted_income=formatted_income,
            formatted_expenses=formatted_expenses,
            currency_form=currency_form,
            display_currency=display_currency
        )

    @app.route('/send_money', methods=['GET', 'POST'])
    @login_required
    def send_money():
        """Send money to another user"""
        form = SendMoneyForm()
        
        if form.validate_on_submit():
            try:
                # Get recipient by email or phone
                recipient = User.query.filter(
                    (User.email == form.recipient_email.data) | 
                    (User.phone == form.recipient_phone.data)
                ).first()
                
                if not recipient:
                    flash('Recipient not found. Please check the email address or phone number.', 'danger')
                    return render_template('send_money.html', form=form)
                
                if recipient.id == current_user.id:
                    flash('You cannot send money to yourself.', 'danger')
                    return render_template('send_money.html', form=form)
                
                # Get sender's account
                sender_account = current_user.account
                if not sender_account:
                    flash('Your account is not set up properly. Please contact support.', 'danger')
                    return render_template('send_money.html', form=form)
                
                # Check if sender has sufficient balance
                amount = Decimal(str(form.amount.data))
                if sender_account.balance < amount:
                    flash('Insufficient balance. Please add money to your account first.', 'danger')
                    return render_template('send_money.html', form=form)
                
                # Get or create recipient's account
                recipient_account = recipient.account
                if not recipient_account:
                    recipient_account = UserAccount(
                        user_id=recipient.id,
                        balance=0.0,
                        currency=recipient.preferred_currency
                    )
                    db.session.add(recipient_account)
                
                # Convert amount if currencies are different
                converted_amount = amount
                if sender_account.currency != recipient_account.currency:
                    try:
                        converted_amount = convert_amount(
                            amount,
                            sender_account.currency,
                            recipient_account.currency
                        )
                    except Exception as e:
                        logger.error(f"Currency conversion error: {str(e)}")
                        flash('Error converting currency. Please try again later.', 'danger')
                        return render_template('send_money.html', form=form)
                
                # Update balances
                sender_account.balance -= amount
                recipient_account.balance += converted_amount
                
                # Create transaction record for sender
                sender_transaction = Transaction(
                    sender_id=current_user.id,
                    receiver_id=recipient.id,
                    amount=amount,
                    currency=sender_account.currency,
                    status='completed',
                    transaction_type='transfer',
                    description=form.description.data
                )
                db.session.add(sender_transaction)
                
                # Create transaction record for receiver if currencies are different
                if sender_account.currency != recipient_account.currency:
                    receiver_transaction = Transaction(
                        sender_id=current_user.id,
                        receiver_id=recipient.id,
                        amount=converted_amount,
                        currency=recipient_account.currency,
                        status='completed',
                        transaction_type='transfer',
                        description=f"Received {format_currency(amount, sender_account.currency)} (converted to {format_currency(converted_amount, recipient_account.currency)})"
                    )
                    db.session.add(receiver_transaction)
                
                db.session.commit()
                
                flash(f'Successfully sent {format_currency(amount, sender_account.currency)} to {recipient.username}', 'success')
                return redirect(url_for('dashboard'))
                
            except Exception as e:
                db.session.rollback()
                logger.error(f"Error in send_money: {str(e)}")
                flash('An error occurred while processing your transaction. Please try again.', 'danger')
                return render_template('send_money.html', form=form)
            
        # Log form validation errors
        if form.errors:
            logger.error(f"Form validation errors: {form.errors}")
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"{field}: {error}", 'danger')
            
        return render_template('send_money.html', form=form)

    @app.route('/add_money', methods=['GET', 'POST'])
    @login_required
    def add_money():
        """Add money to user's account"""
        form = AddMoneyForm()
        
        if form.validate_on_submit():
            try:
                # Get user's account
                account = current_user.account
                if not account:
                    account = UserAccount(
                        user_id=current_user.id,
                        balance=0.0,
                        currency=current_user.preferred_currency
                    )
                    db.session.add(account)
                
                # Convert amount to Decimal
                amount = Decimal(str(form.amount.data))
                if amount <= Decimal('0'):
                    flash('Amount must be greater than 0.', 'danger')
                    return render_template('add_money.html', form=form)
                
                # Update balance
                account.balance += amount
                
                # Create transaction record
                transaction = Transaction(
                    sender_id=current_user.id,
                    receiver_id=current_user.id,
                    amount=amount,
                    currency=account.currency,
                    status='completed',
                    transaction_type='deposit',
                    description=f'Added money via {form.source.data}'
                )
                db.session.add(transaction)
                
                db.session.commit()
                
                flash(f'Successfully added {format_currency(amount, account.currency)} to your account', 'success')
                return redirect(url_for('dashboard'))
                
            except Exception as e:
                db.session.rollback()
                logger.error(f"Error in add_money: {str(e)}")
                flash('An error occurred while adding money. Please try again.', 'danger')
                return render_template('add_money.html', form=form)
            
        # Log form validation errors
        if form.errors:
            logger.error(f"Form validation errors: {form.errors}")
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"{field}: {error}", 'danger')
            
        return render_template('add_money.html', form=form)

    @app.route('/profile', methods=['GET', 'POST'])
    @login_required
    def profile():
        """User profile management route"""
        form = ProfileUpdateForm(obj=current_user)
        
        if form.validate_on_submit():
            try:
                # Check if email is being changed and if it's already taken
                if form.email.data != current_user.email:
                    existing_user = User.query.filter_by(email=form.email.data).first()
                    if existing_user:
                        flash('Email already registered. Please use a different email.', 'danger')
                        return render_template('profile.html', form=form)
                
                # Update user profile
                current_user.email = form.email.data
                current_user.first_name = form.first_name.data
                current_user.last_name = form.last_name.data
                current_user.preferred_currency = form.preferred_currency.data
                
                db.session.commit()
                
                flash('Profile updated successfully!', 'success')
                return redirect(url_for('profile'))
                
            except Exception as e:
                logger.error(f"Error in profile update: {e}")
                flash('An error occurred while updating your profile. Please try again.', 'danger')
                return render_template('profile.html', form=form)
                
        return render_template('profile.html', form=form)

    @app.route('/change-currency', methods=['POST'])
    @login_required
    def change_currency():
        """Change display currency in dashboard"""
        form = CurrencyConversionForm()
        
        if form.validate_on_submit():
            session['display_currency'] = form.currency.data
            flash('Display currency updated!', 'success')
            
        return redirect(url_for('dashboard'))

    @app.route('/transactions')
    @login_required
    def transactions():
        """View all transactions"""
        # Get all transactions for the user
        all_transactions = Transaction.query.filter(
            (Transaction.sender_id == current_user.id) | 
            (Transaction.receiver_id == current_user.id)
        ).order_by(Transaction.timestamp.desc()).all()
        
        # Get current display currency
        display_currency = session.get('display_currency', current_user.preferred_currency or 'INR')
        
        # Create currency conversion form
        currency_form = CurrencyConversionForm()
        currency_form.currency.default = display_currency
        currency_form.process()
        
        # Convert transaction amounts for display
        for tx in all_transactions:
            tx.formatted_amount = format_currency(
                convert_amount(tx.amount, tx.currency, display_currency),
                display_currency
            )
        
        return render_template(
            'transactions.html',
            transactions=all_transactions,
            display_currency=display_currency,
            currency_form=currency_form
        )