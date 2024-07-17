from flask import Blueprint

from app import app

user = Blueprint('user', __name__,
                  url_prefix='/profile/')

from .models import *
from .routes import *