from flask import Blueprint
routes = Blueprint('user_control', __name__)
from .users import *