from flask import render_template, redirect, url_for
from flask_login import login_required
from . import main

@main.route('/')
def index():
    """Render the index page"""
    return redirect(url_for('auth.login'))

@main.route('/dashboard')
@login_required
def dashboard():
    """Render the dashboard page"""
    return render_template('main/dashboard.html')
