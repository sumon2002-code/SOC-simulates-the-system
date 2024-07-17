# Standard libs
import sys
# - Standard libs

# Flask libs
from flask import (render_template, request, abort,
                    flash, redirect, url_for, jsonify)
from flask_login import current_user
from sqlalchemy.exc import IntegrityError
# - Flask libs

# Local libs
from . import event as blueprint_event
from .forms import validate_event_form, EventForm
from .models import Event as db_event

from ..memory_management.event import EventManager, _Event
from ..memory_management.group import GroupManager

from utlis.time_convert import string_to_int as time_s_i

sys.path.append("../..")
from mod_user.user.models import User as db_user

from app import db
# - Local libs

@blueprint_event.route('/', methods=['GET', 'POST'])
def manage():
    
    user:db_user = db_user.query.get(current_user.id)
    group_manager = GroupManager(
        pickle_data=user.groups)

    
    # Fill in the group field
    groups = [
        (group.title, group.color)
        for group in group_manager.list_groups]

    # manager_event = EventManager(
    #     pickle_data=current_user.event.events)

    if request.method == 'GET':
        return render_template('application/calendar.html',
        title='Events',
        _groups=groups)



@blueprint_event.route('/add', methods=['GET', 'POST'])
def add():

    if request.method == 'GET':
        return redirect(url_for('event.manage'))

    user:db_user = db_user.query.get(current_user.id)
    group_manager = GroupManager(
        pickle_data=user.groups)

    if request.method == 'POST':
        form_data = request.get_json()
        
        if not validate_event_form(form_data):
            return abort(400)
        # --- End IF ----

        extendedProps:dict = form_data.get('extendedProps')
        
        event_manager = EventManager(
                pickle_data=user.events[0].events)

        
        _calendar = extendedProps.get('calendar')
        if group_manager.groups.get(_calendar):
            group_title = _calendar
        
        # Add New Event
        event_manager.add_event(
            title=form_data.get('title'),
            url=form_data.get('url'),
            description=form_data.get('extendedProps').get('description'),
            start_time= \
                time_s_i(form_data.get('start')),
            end_time= \
                time_s_i(form_data.get('end')),
            reminders=form_data.get('extendedProps').get('reminders') or [],
            group=group_title)
        
        # Seve Data In Pickle
        user.total_event = int(user.total_event) + 1
        user.events[0].events = event_manager.return_events_in_pickle

        try:
            db.session.commit()
            
        except IndentationError:
            db.session.rollback()
            flash('Something went wrong, please try again', category='error')
        
        else:
            flash('Event add successfully', category='success')
            redirect(url_for('event.manage'))
        
        return f'{event_manager.events}'

@blueprint_event.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id:int):
    user:db_user = db_user.query.get(current_user.id)
    
    event_manager = EventManager(
        pickle_data=user.events[0].events)
    
    _selected_event:_Event|None = \
        event_manager.events.get(int(id))

    # EventNot Found 
    if not _selected_event:
        return abort(404)
    # ----

    group_manager = GroupManager(
        pickle_data=user.groups)


    if request.method == 'GET':
        return redirect(url_for('event.manage'))

    # ----

    if request.method == 'POST':
        form_data = request.get_json()
        
        if not validate_event_form(form_data):
            return abort(400)
        # ----
        extendedProps:dict = form_data.get('extendedProps')
        _calendar = extendedProps.get('calendar')
        if group_manager.groups.get(_calendar):
            group_title = _calendar
        # ----
            
        # Update Event
        event_manager.update_event(
            id=int(id),
            title=form_data.get('title'),
            url=form_data.get('url'),
            description=form_data.get('extendedProps').get('description'),

            start_time= \
                time_s_i(form_data.get('start')),
            end_time= \
                time_s_i(form_data.get('end')),
            
            reminders=form_data.get('extendedProps').get('reminders') or [],
            group_title=group_title)

        # Seve Data In Pickle
        current_user.events[0].events = event_manager.return_events_in_pickle

        try:
            db.session.commit()
            
        except IndentationError:
            db.session.rollback()
            flash('Something went wrong, please try again',
                category='error')
        
        else:
            flash('Event edited successfully',
                category='success')
            return redirect(url_for('event.manage'))
    # ----
    
    return redirect(url_for('event.manage'))


@blueprint_event.route('/delete/<int:id>', methods=['GET'])
def remove(id:int):
    user:db_user = current_user
    
    event_manager = EventManager(
        pickle_data=user.events[0].events)
    
    _selected_event:_Event|None = \
        event_manager.events.get(int(id))
    
    # EventNot Found 
    if not _selected_event:
        return abort(404)
    # ----

    event_manager.delete_event(int(id))
    
    # Seve Data In Pickle
    current_user.events[0].events = \
        event_manager.return_events_in_pickle
    
    try:
        db.session.commit()
    
    except IndentationError:
        db.session.rollback()
        flash('Something went wrong, please try again', category='error')
    
    else:
        flash('The event was successfully deleted', category='success')
    
    return redirect(url_for('event.manage'))
    

@blueprint_event.route('/json/get', methods=['GET'])
def send_json():
    from time import time
    user:db_user = db_user.query.get(current_user.id)
    
    group_manager = GroupManager(
        pickle_data=user.groups)

    manager_event = EventManager(
        pickle_data=user.events[0].events)

    response = [
        {
            "id": event.id, 
            "url":  event.url, 
            "title": event.title, 
            "start": int(event.start_time) * 1000, 
            "end": int(event.end_time) * 1000, 
            "allDay": event.all_day, 
            "extendedProps": { 
                "calendar": 
                    group_manager.groups.get(event.group_title).title
                        if group_manager.groups.get(event.group_title)
                        else '',
                "description" : event.description,
                "reminders" : event.reminders
            } 
        }
        for event in manager_event.events.values()


    ]
    return jsonify(response)
