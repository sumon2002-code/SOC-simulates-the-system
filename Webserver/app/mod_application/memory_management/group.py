from pickle import dumps, loads

class _Group(object):
    __slots__ = ['title', 'description', 'color']

    def __init__(self, title:str,
                 description:str, color:str):
        self.title = title
        self.description = description
        self.color = color
    
    def __repr__(self)-> str:
        return f'{self.__class__.__name__} <{self.title} - {self.color}>'


class GroupManager():
    def __init__(self, pickle_data:bytes=None):
        self.groups:dict[int, _Group] = dict()

        # Default
        self.groups['Personal'] = _Group(
                title='Personal',
                description='Personal [Defualt Group]',
                color='danger')
        
        if pickle_data:    
            self.set_groups(loads(pickle_data))


    #  End Function
        
    @property
    def list_groups(self):
        return [group 
                for group in self.groups.values()]
    #  End Function

    @property
    def return_group_in_pickle(self):
        return dumps(self.list_groups)
    #  End Function
        
    def set_groups(self, groups:list[_Group]):
        self.groups = dict()
        for _g in groups : self.groups[_g.title] = _g

    #  End Function
        
    def add_group(self, title:str, color:str,
                 description:str)-> str :

       self.groups[title] = \
            _Group(
                title=title,
                description=description, color=color)
       
       return title
    #  End Function

    def update_group(self, target_title:str,
                     title:str=None, description:str=None,
                     color:str=None)-> None | KeyError:
        
        if not self.groups.get(target_title):
            raise KeyError

        _group = self.groups[target_title]
        _group.title = title or _group.title
        _group.description = description or _group.description
        _group.color = color or _group.color

        self.groups[title] = _group; del _group
    #  End Function
        
    def delete_group(self, title:str)-> KeyError | None:
        if not self.groups.get(title):
            raise KeyError
        del self.groups[title]
    #  End Function

