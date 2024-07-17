# Standard libs
import sys
from datetime import datetime
# ---

# Flask libs
from flask import render_template, abort, request, flash, redirect, url_for
from flask_login import current_user
from sqlalchemy.exc import IntegrityError
# ---

# local libs
from . import task as buleprint_task
from .models import Task as db_task
from .forms import TaskForm

from ..memory_management.task import TasksManager, _Task
from ..memory_management.group import GroupManager, _Group

from utlis.time_convert import string_to_int as Time_SI
from utlis.time_convert import epoch_to_datetime

sys.path.append("../..")
from mod_user.user.models import User as db_user

from app import db
# ---

@buleprint_task.route('/')
def manage():
    filter_group = request.args.get(
        'group', default='all', type=str)
    
    user:db_user = db_user.query.get(current_user.id)

    # Get Datas
    task_manager = TasksManager(
        pickle_data=user.tasks[0].tasks)
    
    group_manager = GroupManager(
        pickle_data=user.groups)

    groups = group_manager.list_groups
    tasks = []

    if filter_group.lower() == 'all':
        tasks = task_manager.list_tasks
    else :
        tasks = [tk 
        for tk in task_manager.list_tasks
        if tk.group_title == filter]
    # ---

    # Create Form
    form = TaskForm()
    form.group.choices = [(group.title, group.title)
        for group in groups]
    # ---

    # Add Group (ALL)
    groups.insert(0, _Group('All', 'All Group', ''))
    # ---

    return render_template('application/to-do.html',
        title='To Do', form=form, groups=groups,
        tasks=task_manager.list_tasks,
        _filter_group=filter_group)
# End Function

@buleprint_task.route('/add', methods=['POST'])
def add():
    form = TaskForm()
    user:db_user = db_user.query.get(current_user.id)
    
    group_manager = GroupManager(
        pickle_data=user.groups)
    
    form.group.choices = [(group.title, group.title)
        for group in group_manager.list_groups]
    
    if request.method == 'GET':
        return redirect(url_for('task.manage'))
    # ---
    
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('The form is invalid', category='error')
            return f'Eror'
            return render_template('application/to-do.html', 
                                    title='To Do', form=form)
        # ---        
        
        task_manager = TasksManager(
            pickle_data=user.tasks[0].tasks)
        

        # Does this group exist? If not, select the default group
        if group_manager.groups.get(form.group.data):
            _group = form.group.data
        # ---

        task_manager.add_task(
            description=form.description.data,
            name=form.title.data,
            group_title=_group,
            time_start=Time_SI(
                str(form.deadline.data), format='%Y-%m-%d'))
        # ---
    
        current_user.total_task = int(current_user.total_task) + 1
        user.tasks[0].tasks = task_manager.return_tasks_in_pickle

        try:
            db.session.commit()

        except IndentationError:
            db.session.rollback()
            flash('Task add failed! Please try again', category='error')

        else:
            flash('task added successfully', category='success')
            return redirect(url_for('task.manage'))
# End Function 

@buleprint_task.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id:int):
    form = TaskForm()
    user:db_user = db_user.query.get(current_user.id)

    task_manager = TasksManager(
        pickle_data=current_user.tasks[0].tasks)
    
    _selected_task = task_manager.tasks.get(int(id))

    # Task Not Found
    if not _selected_task:
        return abort(404)
    # ----

    group_manager = GroupManager(
        pickle_data=current_user.groups)
    
    form.group.choices = [
        (group.title, group.title)
        for group in group_manager.list_groups]

    # Filling the form fields
    if request.method == 'GET':
        form.title.data = _selected_task.name
        form.group.data = _selected_task.group_title
        form.description.data = _selected_task.description
        form.deadline.data = datetime.strptime(
            epoch_to_datetime(
            int(_selected_task.time_start),
            format='%Y-%m-d'),
            '%Y-%m-d')
    # ---

    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('The form is invalid', category='error')
            return render_template('application/to-do.html', 
                                    title='To Do', form=form)
        # ---

        # Does this group exist? If not, select the default group
        if group_manager.groups.get(form.group.data):
            _group = form.group.data
        # ---

        task_manager.update_task(
            id = int(id),
            name = form.title.data,
            time_start= Time_SI(str(form.deadline.data), format='%Y-%m-%d'),
            description=form.description.data,
            group_title = _group)
        # ---

        current_user.tasks[0].tasks = task_manager.return_tasks_in_pickle

        try:
            db.session.commit()

        except IndentationError:
            db.session.rollback()
            flash('Task editing failed! Please try again', category='error')
        
        else:
            flash('The task was edited successfully', category='success')
            return redirect(url_for('task.manage'))
            
    return render_template('application/form-edit-task.html', 
                        title='To Do', form=form)
# End Function

@buleprint_task.route('remove/<int:id>')
def remove(id:int):
    user:db_user = db_user.query.get(current_user.id)

    task_manager = TasksManager(
        pickle_data=current_user.tasks[0].tasks)
    
    _selected_task = task_manager.tasks.get(int(id))

    # Task Not Found
    if not _selected_task:
        return abort(404)
    # ----

    task_manager.delete_task(int(id))

    current_user.tasks[0].tasks = task_manager.return_tasks_in_pickle

    try:
        db.session.commit()
            
    except IndentationError:
        db.session.rollback()
        flash('Something went wrong, please try again', category='error')
    
    else:
        flash('Task delete successfully', category='success')
        redirect(url_for('task.manage'))

    return redirect(url_for('task.manage'))
# End Function

@buleprint_task.route('switching/<int:id>')
def switching(id):
    user:db_user = db_user.query.get(current_user.id)

    task_manager = TasksManager(
        pickle_data=current_user.tasks[0].tasks)
    
    _selected_task = task_manager.tasks.get(int(id))

    # Task Not Found
    if not _selected_task:
        return abort(404)
    # ----

    task_manager.done_task(id)

    if task_manager.tasks.get(id).done:
        current_user.total_task_done = current_user.total_task_done + 1
    
    current_user.tasks[0].tasks = task_manager.return_tasks_in_pickle

    try:
        db.session.commit()
            
    except IndentationError:
        db.session.rollback()
        flash('Something went wrong, please try again', category='error')
    
    else:
        flash('Change the status of the task successfully', category='success')
        redirect(url_for('task.manage'))

    
    return redirect(url_for('task.manage'))