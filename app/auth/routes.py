import json
import uuid
from flask import render_template, redirect, url_for, flash, request, redirect
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from . import auth
from .user import User

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login
    GET: Display login form
    POST: Process login attempt
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.get_by_username(username)
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        
        flash('Invalid username or password')
    return render_template('auth/login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle user registration
    GET: Display registration form
    POST: Process registration attempt
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if User.get_by_username(username):
            flash('Username already exists')
            return redirect(url_for('auth.register'))
        
        try:
            with open('users.json', 'r') as f:
                users = json.load(f)
        except FileNotFoundError:
            users = {}
        
        user_id = str(uuid.uuid4())
        users[user_id] = {
            'username': username,
            'password_hash': generate_password_hash(password)
        }
        
        with open('users.json', 'w') as f:
            json.dump(users, f, indent=4)
        
        flash('Registration successful! Please login.')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@auth.route('/logout')
@login_required
def logout():
    """Handle user logout"""
    logout_user()
    return redirect(url_for('auth.login'))
