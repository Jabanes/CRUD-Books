from flask import Blueprint, jsonify, request
from crud import *

home_page = Blueprint('home_page', __name__)

@home_page.route('/')
def homePage():
    return 'HOME PAGE'