# Flask libs
from flask import render_template, request, abort, flash, redirect, url_for, jsonify
from flask_login import current_user
from sqlalchemy.exc import IntegrityError
# - Flask libs

# Local libs
from . import group as buleprint_group
from .forms import GroupForm
from ..memory_management.group import GroupManager
from ..memory_management.event import EventManager
from ..memory_management.task import TasksManager

from utlis.dictionary import COLORs as COLORS
from app import db
# - Local libs

COLORs = COLORS()

@buleprint_group.route('/', methods=['GET'])
def manage():
    group_manager = GroupManager(
        pickle_data=current_user.groups)
    form = GroupForm()

    return render_template('application/group.html',
        title='Groups', form=form,
        groups=group_manager.list_groups,
        colors_dict=COLORs.colors_bootstrap)


@buleprint_group.route('/add', methods=['GET', 'POST'])
def add():
    form = GroupForm()
    
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('Invalid forum', category='error')
            return redirect(url_for('group.manage'))
        # ----

        group_manager = GroupManager(
            pickle_data=current_user.groups)
        

        group_manager.add_group(
            title=form.title.data,
            color=form.color.data,
            description=form.description.data)
        
        # Save data in the database with (pickled) format
        current_user.groups = group_manager.return_group_in_pickle

        try:
            db.session.commit()

        except IndentationError:
            db.session.rollback()
            flash('Something went wrong, please try again', category='error')
        
        else:
            flash('New group successfully created', category='success')
            redirect(url_for('group.manage'))
    # ----
    return redirect(url_for('group.manage'))
# End Function

@buleprint_group.route('/edit/<string:title>', methods=['GET', 'POST'])
def edit(title:str):
    form = GroupForm()
    user:db_user = current_user
    
    event_manager = EventManager(
        pickle_data=user.events[0].events)
    
    task_manager = TasksManager(
        pickle_data=current_user.tasks[0].tasks)
    
    group_manager = GroupManager(
        pickle_data=current_user.groups)
    
    _selected_group = group_manager.groups.get(str(title))

    # Group Not Found
    if not _selected_group :
        return abort(404)
    # ----

    if request.method == 'GET':
        form.title.data = _selected_group.title
        form.description.data = _selected_group.description
        form.color.data = _selected_group.color
    # ----

    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('Invalid forum', category='error')
            return render_template('application/form-edit-group.html', 
            title='Edit Group', form=form)
        # ----

        group_manager.update_group(
            target_title=title,
            title=form.title.data,
            color=form.color.data,
            description=form.description.data)

        # Edit events with this group
        for event in event_manager.list_events:
            if event.group_title == title:
                event.group_title = form.title.data

        # Edit task with this group
        for task in task_manager.list_tasks:
            if task.group_title == title:
                task.group_title = form.title.data
        
        # Save data in the database with (pickled) format
        current_user.groups = group_manager.return_group_in_pickle
        
        current_user.tasks[0].tasks = \
            task_manager.return_tasks_in_pickle
        
        current_user.events[0].events = \
            event_manager.return_events_in_pickle
        
        try:
            db.session.commit()
            
        except IndentationError:
            db.session.rollback()
            flash('Something went wrong, please try again', category='error')

        else:
            flash('Group edited successfully', category='success')
            return redirect(url_for('group.manage'))
    # ----
    return render_template('application/form-edit-group.html', 
                            title='Edit Group', form=form)
# End Function

@buleprint_group.route('/remove/<string:title>', methods=['GET'])
def remove(title:str):
    user:db_user = current_user
    
    event_manager = EventManager(
        pickle_data=user.events[0].events)
    
    task_manager = TasksManager(
        pickle_data=current_user.tasks[0].tasks)
    
    group_manager = GroupManager(
        pickle_data=current_user.groups)
    
    # Group Not Found
    if not group_manager.groups.get(str(title)):
        flash('Not Found Group, 404!', category='error')
        return redirect(url_for('group.manage'))
    # ----
    
    # Delete events with this group
    for event in event_manager.list_events:
        if event.group_title == title:
            event_manager.delete_event(int(event.id))
    # ---

    # Delete task with this group
    for task in task_manager.list_tasks:
        if task.group_title == title:
            task_manager.delete_task(int(task.id))
    # ---

    # Delete Group
    group_manager.delete_group(str(title))
    # ---

    # Save data in the database with (pickled) format
    current_user.groups = \
        group_manager.return_group_in_pickle

    current_user.tasks[0].tasks = \
        task_manager.return_tasks_in_pickle
    
    current_user.events[0].events = \
        event_manager.return_events_in_pickle
    # --- (End Seve)
    
    try:
        db.session.commit()
            
    except IndentationError:
        db.session.rollback()
        flash('Something went wrong, please try again', category='error')
    
    else:
        flash('Group delete successfully', category='success')
    
    return redirect(url_for('group.manage'))
# End Function

@buleprint_group.route('/json/get', methods=['GET'])
def send_json():
    group_manager = GroupManager(
        pickle_data=current_user.groups)
    
    data = {
        group.title : group.color
        for group in group_manager.groups.values()
        }
    
    return jsonify(data)