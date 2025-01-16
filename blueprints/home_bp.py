from venv import logger
from flask import Blueprint, request, send_from_directory
from crud import *

home_page = Blueprint('home_page', __name__)

@home_page.route('/')
def homePage():
    logger.info(f"Home page accessed from IP: {request.remote_addr}")
    return send_from_directory('../Frontend', "index.html")