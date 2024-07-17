from sqlalchemy import Column, Integer, String, ForeignKey, Text
from datetime import datetime
from flask_login import UserMixin

from app import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, unique=True, primary_key=True)
    full_name = Column(String(128), unique=False, nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    password = Column(String(256), unique=False, nullable=False)
    roll = Column(Integer, default=0, unique=False)
    groups = Column(Text, nullable=False, unique=False)
    tasks = db.relationship('Task', backref='user')
    events = db.relationship('Event', backref='user')

    total_task = Column(Integer, default=0)
    total_task_done = Column(Integer, default=0)
    total_event = Column(Integer, default=0)

    def __init__(self, full_name:str, email:str, password:str,
                 roll:int=0) -> None:
        
        self.full_name = full_name
        self.email = email
        self.password = password
        self.roll = roll

    def __repr__(self):
        return f'{self.__class__.__name__}< id:{self.id} - email:{self.email} - roll:{self.roll}>'
# End

class Task(db.Model):
    __tablename__ = 'tasks'
    id = Column(Integer, unique=True, primary_key=True)
    tasks = Column(Text, unique=False, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)

    def __init__(self, tasks:bytes):
        self.tasks:bytes = tasks
    
    def __repr__(self):
        return f'{self.__class__.__name__}< id:{self.id} - user_id:{self.user_id} >'
# End

class Event(db.Model):
    __tablename__ = 'events'
    id = Column(Integer, unique=True, primary_key=True)
    events = Column(Text, unique=False, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)

    def __init__(self, events:bytes):
        self.events:bytes = events

    def __rapr__(self):
        return f'{self.__class__.__name__} < id:{self.id} - user_id{self.user_id} >'
# End

class NotUserAuthenticated(db.Model):
    __tablename__ = 'not_user_authenticated'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False)

    def __init__(self, user_id:int)->None:
        self.user_id:int = user_id
    
    def __rapr__(self):
        return f'{self.__class__.__name__} <ID:{self.id} - USER-ID:{self.user_id}>'
# End


