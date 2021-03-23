#!/usr/bin/python

from flask import Flask, redirect, render_template, url_for, request, session
from markupsafe import escape

from extensions import db

from home.home import home_bp
from anime.anime import anime_bp
from scans.scans import scans_bp

from config import Config

def create_app():
    app = Flask(__name__.split('.')[0])
    app.config.from_object(Config)
    register_extensions(app)
    return app

def register_extensions(app):
    db.init_app(app)
    app.register_blueprint(home_bp)
    app.register_blueprint(anime_bp, url_prefix='/anime')
    app.register_blueprint(scans_bp, url_prefix='/scans')

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0')
