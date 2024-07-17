"""
Events manager

- Add Event
- Update Event
- Remove Event
- Making a pickle to store in the database

"""

from pickle import loads, dumps

try:
    from .group import _Group
except ImportError:
    from group import _Group


class _Event():
    __slots__ = ['id', 'title', 'description', 'start_time',
                 'end_time', 'url', 'group_title', 'reminders', 'all_day']
    
    def __init__(self, id:int, title:str, description:str,
                 start_time:int, end_time:int, group:None|_Group,
                 reminders:list[int], url:str, all_day:bool=False):
        self.id = id
        self.title = title
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        self.reminders = reminders
        self.url = url
        self.all_day = all_day

        if group : self.group_title = group
        else : self.group_title = 'Personal'
    
    def __repr__(self)-> str:
        return f'{self.__class__.__name__} <{self.id} - {self.title}>'


class EventManager():
    def __init__(self, pickle_data:bytes=None):
        self.events:dict[int, _Event] = dict()
        self.last_id = 0

        if pickle_data:
            self.set_events(
                loads(pickle_data))
        
    #  End Function
        
    @property
    def list_events(self):
        return [event 
                for event in self.events.values()]
    #  End Function

    @property
    def return_events_in_pickle(self):
        return dumps(self.list_events)
    #  End Function

    def set_events(self, events:list[_Event]):
        for event in events : self.events[event.id] = event
        self.last_id = len(self.events)
    #  End Function

    def add_event(self, title:str, description:str,
                 start_time:int, end_time:int, group:None,
                 reminders:list[int], url:str, all_day:bool=False):
        
        while True:
            self.last_id += 1
            if not self.events.get(self.last_id):
                break
        
        self.events[self.last_id] = \
            _Event(
                id=self.last_id, title=title, group=group,
                description=description, end_time=end_time,
                start_time=start_time, reminders=reminders,
                url=url,all_day=all_day)
    #  End Function

    def delete_event(self, id:int):
        if self.events.get(id):
            del self.events[id]
    #  End Function

    def update_event(self, id:int,
                     title:str=None, reminders:list[int|str]=None,
                     description:str=None, start_time:int=None,
                     end_time:int=None, group_title:None=0,
                     url:str=None, all_day:bool=None)-> None | KeyError:
        
        if not self.events.get(id):
            raise KeyError
        
        _event = self.events[id]
        _event.title = title or _event.title
        _event.description = description or _event.description
        _event.url = url or _event.url
        _event.start_time = start_time or _event.start_time
        _event.end_time = end_time or _event.end_time
        _event.group_title = group_title or _event.group_title
        _event.reminders = reminders or _event.reminders
        if _event.all_day != None:
            _event.all_day = all_day
        # Save
        self.events[id] = _event ; del _event
    #  End Function

if __name__ == '__main__':
    event_manager = EventManager()
