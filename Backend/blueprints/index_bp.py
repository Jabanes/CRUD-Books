from venv import logger
from flask import Blueprint, request, send_from_directory
from crud import *

index_page = Blueprint('index_page', __name__)

@index_page.route('/')
def indexPage():
    logger.info(f"index page accessed from IP: {request.remote_addr}")
    return send_from_directory('../Frontend', "index.html")