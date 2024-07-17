from flask import Blueprint

group = Blueprint('group', __name__, url_prefix='/group/')

from .routes import *

from utlis.flask_login import login_required

@group.before_request
@login_required('group.manage')
def login_required_group()->None:
    pass