#!/usr/bin/python

from flask import Blueprint

home_bp = Blueprint('home_bp', __name__, template_folder='templates')

from app.home import routes
