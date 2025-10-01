from flask import Blueprint

home_bp = Blueprint("home_bp", __name__)

@home_bp.route("/")
def home():
    return "Welcome to the home page! From Blueprint"