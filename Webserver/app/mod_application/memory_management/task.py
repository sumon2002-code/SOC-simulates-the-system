""" 
Manages tasks (Tasks)

- Add Task
- Update Task
- Remove
- Done Task
- Making a pickle to store in the database

"""
from pickle import loads, dumps

try:
    from .group import _Group
except ImportError:
    from group import _Group

class _Task:
    __slots__ = ["id", "name", "time_start", "done", "group_title", "description"]
    def __init__(self, id:int, group_title:str|None,
                 name:str , time_start:int,
                 description:str='', done:bool=False)-> None:
        self.id = id
        self.name = name
        self.time_start = time_start
        self.done = done
        self.description=description
        if group_title : self.group_title = group_title
        else : self.group_title = 'Personal'
    
    def __rper__(self):
        return f'{self.__class__.__name__} <{self.name}, {self.done}>'


class TasksManager:
    def __init__(self, pickle_data:bytes=None):
        self.tasks:dict[int, _Task] = dict()
        self.last_id = 0

        if pickle_data:
            self.set_tasks(loads(pickle_data))

    #  End Function
    
    @property
    def list_tasks(self)-> list[_Task]:
        return [
            task for task in self.tasks.values()]

    @property
    def return_tasks_in_pickle(self)-> str:
        return dumps(self.list_tasks)
    #  End Function

    def set_tasks(self, tasks:list[_Task] )-> None:
        for task in tasks: self.tasks[task.id] = task
        self.last_id = len(self.tasks)
    #  End Function
        
    def add_task(self, name:str,
                time_start:int,
                description:str='',
                group_title:str=None)-> None:
        
        while True:
            self.last_id += 1
            if not self.tasks.get(self.last_id):
                break



        self.tasks[self.last_id] = _Task(id=self.last_id ,name=name,
                            time_start=time_start,
                            description=description,
                            group_title=group_title)
    #  End Function
        
    def done_task(self, id:int):
        self.tasks[id].done = not self.tasks[id].done
    #  End Function
        
    def update_task(self,
                    id:int, name:str=None,
                    time_start:int=None,
                    description:str='',
                    group_title:str=''):
        _task = self.tasks.get(id)
        _task.name = name or _task.name
        _task.description = description or _task.description
        _task.time_start = time_start or _task.time_start
        _task.group_title = group_title or _task.group_title
        


        self.tasks[id] = _task; del _task
    #  End Function 
        
    def delete_task(self, id:int)-> None:
        del self.tasks[id]
    #  End Function
        
if __name__ == '__main__':
    t = TasksManager()
    t.add_task('a', 545)
    print(t.tasks[1].done)
    t.done_task(1)
    print(t.tasks[1].done)
    t.done_task(1)
    print(t.tasks[1].done)