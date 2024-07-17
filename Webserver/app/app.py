from flask import Flask, render_template

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail

from redis import Redis

from config import Configs

app = Flask(__name__, template_folder='templates')
app.config.from_object(Configs)

db = SQLAlchemy()
db.init_app(app=app)

login_manager = LoginManager(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
redis = Redis.from_url(Configs.REDIS_SERVER_URL)

mail = Mail()
mail.init_app(app)
mail.server = Configs.MAIL_SERVER
mail.password = Configs.MAIL_PASSWORD
mail.port = Configs.MAIL_PORT
mail.username = Configs.MAIL_USERNAME


from mod_user.user import user
from mod_user.admin import admin

from mod_application.task import task
from mod_application.group import group
from mod_application.event import event

app.register_blueprint(admin)
app.register_blueprint(user)
app.register_blueprint(group)
app.register_blueprint(task)
app.register_blueprint(event)


from utlis.time_convert import epoch_to_datetime as EpochToDatetime
from utlis.flask_login import login_required

@app.template_global()
def epoch_to_datetime(epochTime, format='%Y-%m-%d', _division:int=1):
    return EpochToDatetime(int(epochTime)/ _division, format)

@app.template_global()
def MAIL_USERNAME():
    return str(Configs.MAIL_USERNAME)

@app.route('/')
@login_required(_next_url='/')
def index():
    return render_template('application/home.html', title='Home')



