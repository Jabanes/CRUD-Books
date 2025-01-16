from venv import logger
from flask import Blueprint, request, send_from_directory
from crud import *

home_page = Blueprint('home_page', __name__)

@home_page.route('/home')
def homePage():
    logger.info(f"home page accessed from IP: {request.remote_addr}")
    return send_from_directory('../Frontend', "home.html")