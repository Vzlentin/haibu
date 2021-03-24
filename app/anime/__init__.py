#!/usr/bin/python

from flask import Blueprint

anime_bp = Blueprint('anime_bp', __name__, static_folder='static', template_folder='templates')

from app.anime import routes
