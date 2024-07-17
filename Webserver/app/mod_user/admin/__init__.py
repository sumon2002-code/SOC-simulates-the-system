from flask import Blueprint

from app import app

admin = Blueprint('admin', __name__,
                  url_prefix='/admin/')

from .models import *
from .routes import *