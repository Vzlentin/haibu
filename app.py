#!/usr/bin/python

from flask import Flask, redirect, render_template, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape

from blueprints.anime import anime_app
from blueprints.scans import scans_app

from config import Config
from models import Bookmarks

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(anime_app, url_prefix='/anime')
app.register_blueprint(scans_app, url_prefix='/scans')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('home'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/test')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'

if __name__ == "__main__":
    app.run(host='0.0.0.0')
