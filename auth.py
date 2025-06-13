import json
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import re

auth_bp = Blueprint('auth', __name__)

# JSON file for storing user data
USERS_FILE = 'users.json'

def load_users():
    """Load users from JSON file"""
    if not os.path.exists(USERS_FILE):
        return {"users": []}
    
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"users": []}

def save_users(users_data):
    """Save users to JSON file"""
    with open(USERS_FILE, 'w') as f:
        json.dump(users_data, f, indent=2)

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def user_exists(email):
    """Check if user with email already exists"""
    users_data = load_users()
    return any(user['email'].lower() == email.lower() for user in users_data['users'])

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handle user signup"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        errors = []
        
        if not name:
            errors.append('Name is required')
        
        if not email:
            errors.append('Email is required')
        elif not validate_email(email):
            errors.append('Please enter a valid email address')
        elif user_exists(email):
            errors.append('An account with this email already exists')
        
        if not password:
            errors.append('Password is required')
        elif len(password) < 6:
            errors.append('Password must be at least 6 characters long')
        
        if not confirm_password:
            errors.append('Please confirm your password')
        elif password != confirm_password:
            errors.append('Passwords do not match')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('auth/signup.html', name=name, email=email)
        
        # Create new user
        users_data = load_users()
        new_user = {
            'name': name,
            'email': email,
            'password': password  # Plain text as requested for now
        }
        users_data['users'].append(new_user)
        save_users(users_data)
        
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/signup.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        
        # Validation
        if not email or not password:
            flash('Please enter both email and password', 'error')
            return render_template('auth/login.html', email=email)
        
        # Check credentials
        users_data = load_users()
        user = None
        for u in users_data['users']:
            if u['email'].lower() == email and u['password'] == password:
                user = u
                break
        
        if user:
            # Set session
            session['user_id'] = user['email']
            session['user_name'] = user['name']
            flash(f'Welcome back, {user["name"]}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'error')
            return render_template('auth/login.html', email=email)
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    """Handle user logout"""
    session.clear()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('auth.login'))

def login_required(f):
    """Decorator to require login for certain routes"""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function