#!/usr/bin/python

from flask import Flask

from config import Config
from extensions import db

from app.home import home_bp
from app.anime import anime_bp
from app.scans import scans_bp

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

app = create_app()
