#!/usr/bin/python

from flask import Blueprint, redirect, render_template, request, session, url_for

home_bp = Blueprint('home_bp', __name__, template_folder='templates')

@home_bp.route('/')
def home():
    return render_template('home/home.html')

@home_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('home_bp.home'))
    return render_template('home/login.html')

@home_bp.route('/test')
def index():
    if 'username' in session:
        return f"Logged in as {session['username']}"
    return 'You are not logged in'
