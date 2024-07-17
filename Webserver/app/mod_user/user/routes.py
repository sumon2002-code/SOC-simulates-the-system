# Flask libs
from flask import (flash, url_for, redirect,
                    render_template, abort, request)
from flask_login import login_user, logout_user, current_user
from sqlalchemy.exc import IntegrityError
# ---

# Local libs
from . import user
from .models import User, NotUserAuthenticated
from .forms import LoginForm, RegisterForm, SettingForm
from .utlis import add_to_redis, get_from_redis, delete_from_redis, send_registration_message

from app import db, bcrypt, Configs

from utlis.flask_login import not_logged_in, login_required
from mod_application.memory_management.group import GroupManager
from mod_application.memory_management.task import TasksManager
from mod_application.memory_management.event import EventManager

from dateabase_models._models import Event, Task
# ---

@user.route('/', methods=['GET'])
@login_required('user.profile')
def profile():
    user:User = current_user
    
    # Has the user confirmed her email?
    user_not_auth = NotUserAuthenticated.query.filter(
            NotUserAuthenticated.user_id.like(user.id)).first()

    if user_not_auth:
        return redirect(url_for('user.confirm_registration'))

    task_total, task_done_total = user.total_task, user.total_task_done
    event_total, event_done_total = user.total_event, user.total_event

    return render_template(
        'user/profile.html', title='Profile', 
        task_total=task_total, task_done_total=task_done_total,
        event_total=event_total, event_done_total=event_total)
# End Function

@user.route('login/', methods=['GET', 'POST'])
@not_logged_in('user.profile')
def login():
    form = LoginForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('Email or password is not valid!!!')
            return render_template('user/forms-A.html', title='Login', form=form)
        # ---

        user = User.query.filter(User.email.ilike(f'{form.email.data}')).first()
        if not user: # Not Found User
            flash("Something went wrong. Please try again")
            return render_template('user/forms-A.html', title='Login', form=form)
        # ---

        login_user(user, remember=form.remember.data)

        # Has the user confirmed her email?
        user_not_auth = NotUserAuthenticated.query.filter(
                NotUserAuthenticated.user_id.like(user.id)).first()

        if user_not_auth:
            return redirect(url_for('user.confirm_registration'))
        # ---
        
        flash('You have successfully logged in' , 'info')
        
        __next = request.args.get('next', type=str,
                                  default=url_for('user.profile'))
        return redirect(__next)
    # ---
    return render_template('user/forms-A.html',
                title='Login', form=form)
# End Function

@user.route('register/', methods=['GET', 'POST'])
@not_logged_in('user.profile')
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('The information is invalid')
            return render_template('user/forms-A.html', title='Register', form=form)
        # ---

        # Remaining: Email confirmation must be added
        NewUser = User(
            full_name=form.full_name.data,
            email=form.email.data,
            password=bcrypt.generate_password_hash(
                            password=form.password.data))
        # ---

        NewUser.groups = GroupManager().return_group_in_pickle
        
        # Create Roll Task And Event 
        NewTask = Task(
            TasksManager().return_tasks_in_pickle)
        NewEvent = Event(
            TasksManager().return_tasks_in_pickle)
        # ---

        # Create Relation 
        NewTask.user = NewUser
        NewEvent.user = NewUser
        # ---
        try:
            db.session.add_all([NewEvent, NewTask, NewUser])
            db.session.commit()
            
            # Add new user to unauthenticated users
            db.session.add(NotUserAuthenticated(NewUser.id))
            db.session.commit()
            # ---
        except IntegrityError:
            db.session.rollback()
            flash('Error! Try again (probably because the email you entered already exists)')
            return render_template('user/forms-A.html', title='Register', form=form)

        else:
            flash('Your account has been created successfully')
            return redirect(url_for('user.login'))

    return render_template('user/forms-A.html', 
                    title='Register', form=form)
# End Function

@user.route('logout/', methods=['GET'])
@login_required()
def logout():
    logout_user()
    flash('Logout was successful.')
    return redirect('/')
# End Function

@user.route('settings/', methods=['GET', 'POST'])
@login_required(_next_endpoint='user.settings')
def settings():
    form  = SettingForm()
    user:User = current_user

    if request.method == 'GET':
        form.email.data = user.email
        form.full_name.data = user.full_name
        
        form.old_password.data, form.password.data,\
            form.confirm_password.data  = '*'*8, '*'*8, '*'*8
        
    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('user/settings.html', title='Setting Account',
                        form=form, submit_button='Update')
        
        user.full_name = form.full_name.data

        # Checks that in the password fields ([not 8 stars] : '*'*8 )
        _password_not_asterisk = '*'*8 in [form.confirm_password.data, 
                                           form.old_password.data, form.password.data]
        
        # Checks that the user has entered the account password correctly
        _password_must_be_correct = bcrypt.check_password_hash(
                                    user.password, form.old_password.data)\
                                    if not _password_not_asterisk else False
        
        if _password_must_be_correct :
            user.password = bcrypt.generate_password_hash(form.password.data)
        # ---

        if form.email.data != user.email:
            # Remaining: Email confirmation must be added
            user.email = form.email.data
            # Add new user to unauthenticated users
            db.session.add(NotUserAuthenticated(user.id))
        # ---

        try:
            db.session.commit()
        except IntegrityError:
            flash('Updating your profile information failed! Please try again.')
            db.session.rollback()
        else:
            flash('Your profile information has been successfully updated .')
            
            if _password_must_be_correct:
                flash('Your password has been successfully updated .')

    return render_template('user/settings.html', title='Setting Account',
                           form=form, submit_button='Update')
# End Function

@user.route('/delete', methods=['GET'])
@login_required('user.profile')
def delete():
    user:User = User.query.get(current_user.id)
    
    for event in user.events : db.session.delete(event)
    for task in user.tasks : db.session.delete(task)

    db.session.delete(user)
    db.session.commit()

    return redirect(url_for('user.login'))
# End Function


@user.route('/confirm/')
@login_required('user.confirm_registration')
def confirm_registration():
    
    # Get Datas
    email = current_user.email
    resend = request.args.get(key='resend')
    token = request.args.get(key='token', type=str)

    # To resend the email
    if resend :
        # for beauty and not sending flash messages
        if token:
            return redirect(
                url_for('user.confirm_registration', token=token))
        # ---
        flash('The authentication email has been re-sent to your email address')
    # ---

    # Request without arguments
    if (not token):
        """
        If you send a request to this room without a token argument 
        (an authentication token will be created and sent)
        """
        token = add_to_redis(current_user, 'register')
        send_registration_message(current_user, token)
        
        return render_template('user/email-confirmation-required.html',
        msg=f"""Account activation link sent to your email address: 
                {Configs.MAIL_USERNAME} 
                Please follow the link inside to continue.""")
    # ---

    user_auth = NotUserAuthenticated.query.filter(
        NotUserAuthenticated.user_id.like(current_user.id)).first()

    # If the user is active    
    if not user_auth:
        return render_template(
            'user/email-confirmation-required.html',
            msg=f"This user is already activated. <br> <a href='{url_for('user.profile')}'>Profile</a>")
    # ---

    # Checking the validity of the token
    token_from_redis = get_from_redis(current_user, 'register')
    
    if (not token_from_redis) or \
        (str(token) != token_from_redis.decode('UTF-8')):
        return render_template(
            'user/email-confirmation-required.html',
            msg=f"The token has expired!")
    # ---

    # Activate the user
    delete_from_redis(current_user, 'register')
    db.session.delete(user_auth)
    db.session.commit()
    # ---

    flash('Your email has been successfully verified! welcome')
    return redirect(url_for('user.profile'))
# End Function
    






