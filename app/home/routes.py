#!/usr/bin/python

from flask import redirect, render_template, request, session, url_for

from app.home import home_bp

@home_bp.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST' and 'username' in request.form:
        session['username'] = request.form['username']
    return render_template('home/home.html')
