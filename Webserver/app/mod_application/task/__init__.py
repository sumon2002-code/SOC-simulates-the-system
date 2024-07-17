from flask import Blueprint

from app import app

task = Blueprint('task', __name__,
                 url_prefix='/task/')

from .models import *
from .routes import *

from utlis.flask_login import login_required

@task.before_request
@login_required('task.manage')
def login_required_task()->None:
    pass