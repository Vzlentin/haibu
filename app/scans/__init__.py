#!/usr/bin/python

from flask import Blueprint

scans_bp = Blueprint("scans_bp", __name__, static_folder='static', template_folder='templates')

from app.scans import routes
