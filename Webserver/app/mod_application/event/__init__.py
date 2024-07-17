from flask import Blueprint

event = Blueprint('event', __name__, url_prefix='/event/')

from .routes import *

from utlis.flask_login import login_required

@event.before_request
@login_required('event.manage')
def login_required_event()->None:
    pass