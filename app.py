#!/usr/bin/python

from flask import Flask, redirect, render_template, url_for, request
from blueprints.anime import anime_app
from blueprints.scans import scans_app

app = Flask(__name__)
app.register_blueprint(anime_app, url_prefix='/anime')
app.register_blueprint(scans_app, url_prefix='/scans')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)
