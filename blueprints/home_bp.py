from venv import logger
from flask import Blueprint, jsonify, request
from crud import *

home_page = Blueprint('home_page', __name__)

@home_page.route('/')
def homePage():
    print("Home page accessed")  # This will print in the terminal where Flask is running
    logger.info(f"Home page accessed from IP: {request.remote_addr}")
    return "HOME PAGEEEEEE"